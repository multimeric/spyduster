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
    @property
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

    @cached_property
    def next_page_url(self) -> str:
        if isinstance(a := self.content.css.select_one(".list-inline-item.nxt a[href]"), Tag):
            if isinstance(link := a.attrs.get("href"), str):
                return urljoin(self.base_url, link)
        raise ValueError("No next page found")

    def next_page(self) -> Collection:
        return Collection(self.next_page_url, cookies=self.cookies)

    def iter_links(self) -> Iterable[str]:
        """
        Yields the links to the full record pages.

        Interestingly, these links are different each time. It seems that they encode the search query in their URL.

        Params:
            all_pages: If True, the generator will yield links from all subsequent result pages. Otherwise, it will only yield links from the current page.
        """
        for record in self.records_raw:
            if (a := record.css.select_one("a[href]")) is not None:
                if isinstance(link := a.attrs["href"], str):
                    yield urljoin(self.base_url, link)
    
    def iter_all_links(self) -> Iterable[str]:
        coll = self
        i = 0

        while True:
            for link in coll.iter_links():
                yield link
                i += 1
            
            if i == self.count:
                break

            coll = coll.next_page()


    def iter_full_results(self, all_pages: bool = True) -> Iterable[Record]:
        from spydusclient.record import Record

        for link in self.iter_all_links() if all_pages else self.iter_links():
            yield Record(link, cookies=self.cookies)
