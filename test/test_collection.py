from spydusclient.collection import Collection

def test_lotr():
    coll = Collection("https://boroondara.spydus.com/cgi-bin/spydus.exe/REFSET/WPAC/BIBENQ/77735065?FT=BTY&QRY=BFRMT%3A%20BK&SQL=&QRYTEXT=Material%20type%3A%20Books&QFT=BTY&QFV=BK")
    assert coll.count == 4

    links = list(coll.iter_links())
    assert "48159177,1" in links[0]