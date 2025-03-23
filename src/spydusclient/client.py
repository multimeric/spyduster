from dataclasses import dataclass
from urllib.parse import urlunparse, urlencode

from spydusclient.record import Record


@dataclass
class SpydusClient:
    base_url: str

    def get_archive_record(
        self,
        record_id: int
    ) -> Record:
        params = urlencode({
            "RNI": record_id,
            "SETLVL": ""
        })
        return Record(url=urlunparse(
            (self.base_url, "/cgi-bin/spydus.exe/ENQ/WPAC/ARCENQ", params)
        ))

    def get_book(
        self,
        brn: int
    ) -> Record:
        params = urlencode({
            "BRN": brn,
            "SETLVL": ""
        })
        return Record(url=urlunparse(
            (self.base_url, "/cgi-bin/spydus.exe/ENQ/WPAC/BIBENQ", params)
        ))