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
        """
        Yields the raw HTML elements of the records in the collection that are displayed on the current page.
        Note that this does not include subsequent pages, but you can use the [`next_page`][next_page] method to get the next page.
        """
        if (isinstance(content := self.content.find(id="result-content-list"), Tag)):
            for child in content.children:
                if isinstance(child, Tag):
                    yield child

    @cached_property
    def count(self) -> int:
        """
        The total number of records in the collection.
        Note that this is not the number of records displayed on the current page.
        """
        if isinstance(header := self.content.css.select_one(".result-header-brief"), Tag):
            if (match := COUNT.search(header.text)) is not None:
                return int(match.group(1))
        raise ValueError("No count found")

    @cached_property
    def next_page_url(self) -> str:
        """
        Link to the next page of the collection.
        If there is no next page, this fails with a ValueError.
        """
        if isinstance(a := self.content.css.select_one(".list-inline-item.nxt a[href]"), Tag):
            if isinstance(link := a.attrs.get("href"), str):
                return urljoin(self.base_url, link)
        raise ValueError("No next page found")

    def next_page(self) -> Collection:
        """
        A parsed version of the next page of the collection.
        If there is no next page, this fails with a ValueError.
        """
        return Collection(self.next_page_url, cookies=self.cookies)

    def iter_links(self) -> Iterable[str]:
        """
        Yields the links to the full record pages.

        Interestingly, these links are different each time. It seems that they encode the search query in their URL.
        """
        for record in self.records_raw:
            if (a := record.css.select_one("a[href]")) is not None:
                if isinstance(link := a.attrs["href"], str):
                    yield urljoin(self.base_url, link)
    
    def iter_all_links(self) -> Iterable[str]:
        """
        Yield all links to the full record pages in this collection, including those on subsequent pages.
        """
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
        """
        Yields parsed Record objects for all records in the collection.
        """
        from spydusclient.record import Record

        for link in self.iter_all_links() if all_pages else self.iter_links():
            yield Record(link, cookies=self.cookies)
