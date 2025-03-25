from spyduster.collection import Collection

def test_lotr():
    coll = Collection("https://boroondara.spydus.com/cgi-bin/spydus.exe/REFSET/WPAC/BIBENQ/77735065?FT=BTY&QRY=BFRMT%3A%20BK&SQL=&QRYTEXT=Material%20type%3A%20Books&QFT=BTY&QFV=BK")
    assert coll.count == 4

    links = list(coll.iter_links())
    assert "48159177,1" in links[0]

def test_council():
    coll = Collection(r"https://boroondara.spydus.com/cgi-bin/spydus.exe/ENQ/WPAC/ARCENQ/77735706?QRY=ARL03%5C75834999%20%2B%20ARL02%5C40&QRYTEXT=File%20records%20from%20Council%20Meeting%20Agendas%20and%20Minutes%20Hawthorn%20Council%20(1860-1994)&SORTS=ARL.LVL]ARL.SRT]HBT.SOVR")
    assert coll.count == 15
    assert coll.next_page_url.endswith("NREC=10")
    assert sum(1 for _ in coll.iter_links()) == 10, "There should be 10 links on the current page"
    assert sum(1 for _ in coll.iter_all_links()) == 15, "There should be 15 links on all pages"