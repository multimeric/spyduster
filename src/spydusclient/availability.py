
from functools import cached_property
from typing import Iterable
from urllib.parse import urljoin
from spydusclient.base import SpydusPage

class Availability(SpydusPage):
    @cached_property
    def headers(self) -> list[str]:
        """
        The column headers of the availability table.
        """
        if (table := self.content.select_one("table")) is not None:
            if (thead := table.select_one("thead")) is not None:
                return [th.text for th in thead.find_all("th")]
        return []

    @property
    def entries(self) -> Iterable[dict[str, str]]:
        """
        Yields rows of the availability table as dictionaries.
        Keys are the column headers.
        """
        if (tbody := self.content.select_one("table tbody")) is not None:
            for row in tbody.select("tr"):
                yield {header: cell.text for header, cell in zip(self.headers, row.select("td"))}

    @property
    def download_link(self) -> str:
        """
        Finds a download link in the availability table.
        If no download link is found, this fails with a ValueError.
        This only makes sense for digital items.
        """
        if (a := self.content.select_one("tbody a[href]")) is not None:
            if isinstance(href := a.attrs.get("href"), str):
                if "LOGINB" in href or "download" not in href:
                    raise ValueError("Login required")
                return urljoin(self.base_url, href)
        raise ValueError("No download link found. Are you sure this is a digital item?")

