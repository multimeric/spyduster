# from spydusclient.old import get_book, get_archive_record

# def test_record():
#     record = get_book(614180)
#     fields = record.get_properties()
#     assert "So late in the day" in fields["Main title"][0]

# def test_archive_record():
#     record = get_archive_record(3122612)
#     fields = record.get_properties()
#     assert "Council Meeting Agendas and Minutes" in fields["Title"][0]
#     assert "QRYTEXT=Sub-sub-sub-collection" in record._subcollection_link()
    
#     subcoll = record.get_subcollection()
#     assert len(list(subcoll.iter_links())) == 5
