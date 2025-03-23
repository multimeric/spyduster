from __future__ import annotations
from typing import Iterable, Literal
from urllib.parse import urljoin
from pydantic import BaseModel, ConfigDict
import requests
from typer import Typer
from enum import Enum
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag
import json
# from bs4._typing import _PageE

class Sorts(str, Enum):
    SQL_RANDOM = "SQL_RANDOM"
    HBT_SOVR = "HBT.SOVR"
    MAIN_CREATED_DATE_DESC_MAIN_CREATED_TIME_DESC = "MAIN.CREATED_DATE.DESC]MAIN.CREATED_TIME.DESC"
    ARL_SRT = "ARL.SRT"
    NONE = "NONE"

class Xslt(str, Enum):
    XGalleryDisplay_xsl = "XGalleryDisplay.xsl"
    XBrowseFacets_xsl = "XBrowseFacets.xsl"
    XCmtDisplay_xsl = "XCmtDisplay.xsl"
    XTagDisplay_xsl = "XTagDisplay.xsl"

# from pydantic.alias_generators import 

app = Typer()

BASE = "https://boroondara.spydus.com/"



# class QueryParams(BaseModel):
#     model_config = ConfigDict(
#         alias_generator=str.upper
#     )
#   --data-urlencode 'QRY=ARL03\75834993' \
#   --data-urlencode 'SORTS=ARL.SRT' \
#   --data-urlencode 'XSLT=XGalleryDisplay.xsl' \
#   --data-urlencode 'NRECS=2' \
#   --data-urlencode 'SETID=77504231' \
@app.command()
def fragment(
    qry: str,
    setid: int,
    cookies: str,
    record_number: int = 77505521,
    sorts: Sorts = Sorts.SQL_RANDOM,
    xslt: Xslt = Xslt.XGalleryDisplay_xsl,
    nrecs: int = 20,
):
    res = requests.get(
        # url=f"https://boroondara.spydus.com/cgi-bin/spydus.exe/ENQ/WPAC/ARCENQ/{id}",
        url=f"https://boroondara.spydus.com/cgi-bin/spydus.exe/ENQ/WPAC/ARCENQ",
        params={
        "QRY": qry,
        "SORTS": sorts,
        "XSLT": xslt,
        "NRECS": nrecs,
        "SETID": setid
    }, headers={
        "Cookie": cookies
    })
    soup = bs(res.text, features="html.parser")
    print(soup.prettify())


if __name__ == "__main__":
    app()