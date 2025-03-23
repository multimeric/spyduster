from __future__ import annotations
from typing import TYPE_CHECKING
from urllib.parse import urljoin
from bs4.element import Tag
from functools import cached_property
import re
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
        if (span := self.properties_raw["Includes"].css.select_one("span")) is not None:
            if (match := NUMBER.search(span.text)) is not None:
                return int(match.group())
        return 0

    @cached_property
    def subcollection_link(self) -> str:
        if (tag := self.properties_raw["Includes"].css.select_one("a[href]")) is not None:
            if isinstance(url := tag.attrs["href"], str):
                return urljoin(self.base_url, url)
        raise ValueError("No subcollection link found")

    def get_subcollection(self) -> Collection:
        return Collection(self.subcollection_link)