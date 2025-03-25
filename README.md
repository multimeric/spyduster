# Spyduster

Web scraping client for the Spydus library system.

## Installation

```bash
uv add https://github.com/multimeric/spyduster
```

## Basic Usage

```python
from spyduster import Record, Collection
import json

# Search for books by Jorge Luis Borges.
# Obtain this search URL by using your browser
borges = Collection(r"https://YOUR_LIBRARY.spydus.com/cgi-bin/spydus.exe/ENQ/WPAC/BIBENQ/77999253?QRY=CAUBIB%3C%20IRN(44070117)&QRYTEXT=Borges%2C%20Jorge%20Luis%2C%201899-1986")
for book in borges.iter_full_results():
    print(json.dumps(book.properties, indent=4))
```

Will print something like:

```json
{
    "Main title": [
        "Brodie's report [text] : including the prose fiction from In praise of darkness / Jorge Luis Borges ; translated with an afterword by Andrew Hurley."
    ],
    "Author": [
        "Borges, Jorge Luis, 1899-1986"
    ],
    "Imprint": [
        "London : Penguin, 2000."
    ],
    "Collation": [
        "131 p."
    ],
    "ISBN": [
        "0141183861"
    ],
    "BRN": [
        "224479"
    ]
}
{
    "Main title": [
        "Fictions / Jorge Luis Borges ; translated with an afterword by Andrew Hurley."
    ],
    "Author": [
        "Borges, Jorge Luis, 1899-1986, author",
        "Hurley, Andrew, 1944-, translator, author of afterword, colophon, etc"
    ],
    "Imprint": [
        "London : Penguin Books, 2000.",
        "\u00a91998."
    ],
    "Collation": [
        "178 pages ; 20 cm."
    ],
    "Notes": [
        "These translations originally published in Collected fictions: United States : Viking Penguin, 1998.",
        "Short stories.",
        "Translated from the Spanish."
    ],
    "Contents": [
        "FICTIONS. The garden of  forking paths. Tlon, Uqbar, Orbis tertius -- The approach to Al-Mu'tasim -- Pierre Menard, author of the Quixote -- The circular ruins -- The lottery in Babylon -- A survey of the works of Herbert Quain -- The library of Babel -- The garden of forking paths -- ARTIFICES. Funes, his memory -- The shape of the sword -- The theme of the traitor and the hero -- Death and the compass -- The secret miracle -- Three versions of Judas -- The end -- The cult of the phoenix -- The south."
    ],
    "ISBN": [
        "9780141183848 (paperback)"
    ],
    "Language": [
        "English",
        "Spanish"
    ],
    "Added title": [
        "Ficciones. English. (Hurley)",
        "Collected fictions"
    ],
    "Subject": [
        "Borges, Jorge Luis, 1899-1986 -- Translations into English",
        "Short stories, Argentine -- Translations into English",
        "Argentine fiction -- Translations into English",
        "Argentine literature -- Translations into English"
    ],
    "BRN": [
        "62706"
    ]
}
```
