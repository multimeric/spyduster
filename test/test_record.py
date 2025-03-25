from spyduster import Record

def test_bee_sting():
    rec = Record("https://boroondara.spydus.com/cgi-bin/spydus.exe/ENQ/WPAC/BIBENQ?BRN=607007&CF=BIB&SETLVL=")
    assert "The bee sting" in rec.properties["Main title"][0]
    assert "Murray, Paul" in rec.properties["Author"][0]
    assert "9780241353967" in rec.properties["ISBN"][0]
