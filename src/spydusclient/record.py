from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING, Iterable
from urllib.parse import urljoin
from bs4.element import Tag
from functools import cached_property
import re

from requests import get
from spydusclient.availability import Availability
from spydusclient.base import SpydusPage
from spydusclient.utils import response_filename

NUMBER = re.compile(r"\d+")

if TYPE_CHECKING:
    from spydusclient.collection import Collection

class Record(SpydusPage):


    @cached_property
    def properties_raw(self) -> dict[str, Tag]:
        """
        A dictionary of raw property values for the record.
        Keys are property names such as "Title", "Author" etc, and values are the corresponding HTML tags.
        Unfortunately the keys are not standardized and depend on the record in question.
        """
        details = self.content.find(id="divtabRECDETAILS")
        if not isinstance(details, Tag):
            raise ValueError("Invalid document structure")
        ret: dict[str, Tag] = {}
        for row in details.css.select(".row"):
            key, value = row.children
            if not isinstance(value, Tag):
                continue
            ret[key.text.replace(":", "").strip()] = value
        return ret

    @cached_property
    def properties(self) -> dict[str, list[str]]:
        """
        A dictionary of raw property values for the record.
        Keys are property names such as "Title", "Author" etc, and values are a list of paragraphs corresponding to the property.
        Unfortunately the keys are not standardized and depend on the record in question.
        """
        return {
            key: [el.text for el in value.css.select(".d-block")]
            for key, value in self.properties_raw.items()
        }

    @cached_property
    def subcollection_count(self) -> int:
        """
        The number of subcollections in this record.
        If this is zero, the record likely has no subcollections.
        """
        if (includes := self.properties_raw.get("Includes")) is not None:
            if (span := includes.css.select_one("span")) is not None:
                if (match := NUMBER.search(span.text)) is not None:
                    return int(match.group())
        return 0

    @cached_property
    def subcollection_link(self) -> str:
        """
        The link to the subcollection of this record.
        This is a collection of other records that are make up this record.
        """
        if (tag := self.properties_raw["Includes"].css.select_one("a[href]")) is not None:
            if isinstance(url := tag.attrs["href"], str):
                return urljoin(self.base_url, url)
        raise ValueError("No subcollection link found")

    @property
    def subcollection(self) -> Collection:
        """
        The subcollection of this record, as a Collection object.
        This is a collection of other records that are make up this record.
        """
        from spydusclient.collection import Collection
        return Collection(self.subcollection_link, cookies=self.cookies)

    @cached_property
    def availability_link(self) -> str:
        """
        The link to the availability page for this record.
        """
        if (tag := self.content.css.select_one(".fd-availability a[href][data-toggle=modal]")) is not None:
            if isinstance(url := tag.attrs["href"], str):
                return urljoin(self.base_url, url)
        raise ValueError("No availability link found")
    
    @property
    def full_availability(self) -> Availability:
        """
        The parsed availability page for this record.
        """
        from spydusclient.availability import Availability
        return Availability(self.availability_link, cookies=self.cookies)

    def yield_leaves(self) -> Iterable[Record]:
        """
        Starting with this record, visits all sub records by following the subcollection links.
        Yields records that have no subcollections.
        """
        if self.subcollection_count > 0:
            for subrecord in self.subcollection.iter_full_results():
                yield from subrecord.yield_leaves()
        else:
            yield self

    def yield_downloads(self, out_dir: Path) -> Iterable[Path]:
        """
        Visits all leaf records, and if any of them have a download link, downloads the file to the given directory.
        """
        for record in self.yield_leaves():
            try:
                link = record.full_availability.download_link
                res = get(link, cookies=self.cookies)
                filename = out_dir / response_filename(res)
                filename.write_bytes(res.content)
                yield filename
            except ValueError:
                continue