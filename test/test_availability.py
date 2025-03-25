from spyduster.availability import Availability


def test_availability():
    av = Availability("https://boroondara.spydus.com/cgi-bin/spydus.exe/XHLD/WPAC/ARCENQ/77865461/75835290")
    assert av.headers == [
        "Type",
        "Reference No.",
        "Extent",
        "Status/Desc"
    ]
    entries = list(av.entries)
    assert len(entries) == 1
    assert entries[0]["Type"] == "Original"