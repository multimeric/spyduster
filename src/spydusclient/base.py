from __future__ import annotations
from dataclasses import dataclass, InitVar, field
from typing import Iterable
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from functools import cache, cached_property
import re

@dataclass
class SpydusPage:
    url: str
    content: BeautifulSoup = field(init=False)

    def __post_init__(self):
        res = requests.get(self.url)
        self.content = BeautifulSoup(res.text, features="html.parser")

    @cached_property
    def base_url(self) -> str:
        return urljoin(self.url, "/")