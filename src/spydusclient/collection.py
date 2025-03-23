from __future__ import annotations
from functools import cached_property
from typing import Iterable, TYPE_CHECKING
from urllib.parse import urljoin
from spydusclient.base import SpydusPage
from bs4.element import Tag
import re

if TYPE_CHECKING:
    from spydusclient.record import Record

COUNT = re.compile(r"of (\d+)")

class Collection(SpydusPage):
    @cached_property
    def records_raw(self) -> Iterable[Tag]:
        if (isinstance(content := self.content.find(id="result-content-list"), Tag)):
            for child in content.children:
                if isinstance(child, Tag):
                    yield child

    @cached_property
    def count(self) -> int:
        if isinstance(header := self.content.css.select_one(".result-header-brief"), Tag):
            if (match := COUNT.search(header.text)) is not None:
                return int(match.group(1))
        raise ValueError("No count found")

    def next_page(self) -> Collection:
        if isinstance(a := self.content.css.select_one(".list-inline-item.nxt"), Tag):
            if isinstance(link := a.attrs.get("href"), str):
                return Collection(urljoin(self.base_url, link))
        raise ValueError("No next page found")

    def iter_links(self, all_pages: bool = True) -> Iterable[str]:
        """
        Yields the links to the full record pages.

        Interestingly, these links are different each time. It seems that they encode the search query in their URL.

        Params:
            all_pages: If True, the generator will yield links from all subsequent result pages. Otherwise, it will only yield links from the current page.
        """
        coll = self
        i = 0

        while i < self.count:
            for record in self.records_raw:
                if (a := record.css.select_one("a[href]")) is not None:
                    if isinstance(link := a.attrs["href"], str):
                        yield urljoin(self.base_url, link)
                        i += 1
            if all_pages:
                coll = coll.next_page()


    def iter_full_results(self, all_pages: bool = True) -> Iterable[Record]:
        for link in self.iter_links(all_pages):
            yield Record(link)
