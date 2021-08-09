from quickbase_client import ResponsePager


class TestResponsePager:
    def test_initially_more_remaining(self):
        pager = ResponsePager()
        assert pager.more_remaining()

    def test_more_remaining_if_metadata_says_so(self):
        pager = ResponsePager()
        pager.update_from_metadata(
            {"numFields": 1, "numRecords": 1000, "skip": 0, "totalRecords": 1500}
        )
        assert pager.num_calls > 0
        assert pager.more_remaining()

    def test_no_more_remaining_if_exhausted(self):
        pager = ResponsePager()
        pager.update_from_metadata(
            {"numFields": 1, "numRecords": 500, "skip": 1000, "totalRecords": 1500}
        )
        assert pager.num_calls > 0
        assert not pager.more_remaining()
