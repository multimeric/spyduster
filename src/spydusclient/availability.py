
from functools import cached_property
from typing import Iterable
from spydusclient.base import SpydusPage

# class AvailabilityEntry:

class Availability(SpydusPage):
    @cached_property
    def headers(self) -> list[str]:
        if (table := self.content.select_one("table")) is not None:
            if (thead := table.select_one("thead")) is not None:
                return [th.text for th in thead.find_all("th")]
        return []

    @property
    def entries(self) -> Iterable[dict[str, str]]:
        if (tbody := self.content.select_one("table tbody")) is not None:
            for row in tbody.select("tr"):
                yield {header: cell.text for header, cell in zip(self.headers, row.select("td"))}

    @property
    def download_link(self) -> str:
        if (a := self.content.select_one("tbody a[href]")) is not None:
            if isinstance(href := a.attrs.get("href"), str):
                if "LOGINB" in href:
                    raise ValueError("Login required")
                return href
        raise ValueError("No download link found. Are you logged in?")

