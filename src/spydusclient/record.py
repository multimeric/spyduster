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

NUMBER = re.compile(r"\d+")

if TYPE_CHECKING:
    from spydusclient.collection import Collection

class Record(SpydusPage):
    @cached_property
    def properties_raw(self) -> dict[str, Tag]:
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
        return {
            key: [el.text for el in value.css.select(".d-block")]
            for key, value in self.properties_raw.items()
        }

    @cached_property
    def subcollection_count(self) -> int:
        if (includes := self.properties_raw.get("Includes")) is not None:
            if (span := includes.css.select_one("span")) is not None:
                if (match := NUMBER.search(span.text)) is not None:
                    return int(match.group())
        return 0

    @cached_property
    def subcollection_link(self) -> str:
        if (tag := self.properties_raw["Includes"].css.select_one("a[href]")) is not None:
            if isinstance(url := tag.attrs["href"], str):
                return urljoin(self.base_url, url)
        raise ValueError("No subcollection link found")

    @property
    def subcollection(self) -> Collection:
        from spydusclient.collection import Collection
        return Collection(self.subcollection_link, cookies=self.cookies)

    @cached_property
    def availability_link(self) -> str:
        if (tag := self.content.css.select_one(".fd-availability a[href][data-toggle=modal]")) is not None:
            if isinstance(url := tag.attrs["href"], str):
                return urljoin(self.base_url, url)
        raise ValueError("No availability link found")
    
    @property
    def full_availability(self) -> Availability:
        from spydusclient.availability import Availability
        return Availability(self.availability_link, cookies=self.cookies)

    def yield_leaves(self) -> Iterable[Record]:
        """
        Starting with this record, visits all records by following the subcollection links.
        Yields records that have no subcollections.
        """
        if self.subcollection_count > 0:
            for subrecord in self.subcollection.iter_full_results():
                yield from subrecord.yield_leaves()
        else:
            yield self

    def yield_downloads(self, out_dir: Path) -> Iterable[Path]:
        """
        Saves all downloads to the given directory.
        """
        for record in self.yield_leaves():
            try:
                link = record.full_availability.download_link
                filename = out_dir / f"{record.properties['Title'][0]}.pdf"
                filename.write_bytes(get(link, cookies=self.cookies).content)
                yield filename
            except ValueError:
                continue