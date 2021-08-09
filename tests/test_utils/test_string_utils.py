from quickbase_client.utils.string_utils import id_from_iso_string
from quickbase_client.utils.string_utils import make_unique_var_name
from quickbase_client.utils.string_utils import make_var_name
from quickbase_client.utils.string_utils import normalize_unicode
from quickbase_client.utils.string_utils import parse_realm_and_app_id_from_url


class TestMakeVarName:
    def test_no_preceding_numbers(self):
        v = make_var_name("1abc")
        assert "1" not in v
        assert v == "abc"

    def test_use_underscore_before_numbers(self):
        v = make_var_name("1bc", number_strategy="underscore")
        assert v == "_1bc"

    def test_no_special_chars(self):
        v = make_var_name("abc-123")
        assert "-" not in v

    def test_snake_case_special_char_to_underscore(self):
        v = make_var_name("abc - 123")
        assert v == "abc_123"

    def test_pascal_case_drops_special_chars(self):
        v = make_var_name("abc - 123", case="pascal")
        assert v == "Abc123"

    def test_snake_case(self):
        v = make_var_name("abc def")
        assert v == "abc_def"

    def test_snake_all_caps(self):
        v = make_var_name("ABC")
        assert v == "abc"

    def test_snake_no_duplicate_underscores(self):
        v = make_var_name("a_b_c")
        assert v == "a_b_c"

    def test_no_keywords(self):
        v = make_var_name("yield")
        assert v == "yield_"

    def test_multi_caps(self):
        v = make_var_name("abcCAPS")
        assert v == "abc_caps"

    def test_trailing_special_characters(self):
        v = make_var_name("Is Open?")
        assert v == "is_open"


class TestMakeUniqueVarName:
    def test_make_unique(self):
        taken = ["myvar", "myvar1", "myvar_1", "myvar_2"]
        v = make_unique_var_name("myvar", taken)
        assert v not in taken
        assert "myvar" in v


class TestIdFromIsoString:
    def test_makes_string(self):
        s = id_from_iso_string("2020-10-10T00:00:00.00Z")
        assert s == "2020101000000000"


class TestParseRealmAndAppIdFromUrl:
    def test_parses(self):
        url = "https://dicorp.quickbase.com/db/bqx7xre7a?a=td"
        realm, app_id = parse_realm_and_app_id_from_url(url)
        assert realm == "dicorp.quickbase.com"
        assert app_id == "bqx7xre7a"

    def test_parses_without_protocol(self):
        url = "dicorp.quickbase.com/db/bqx7xre7a?a=td"
        realm, app_id = parse_realm_and_app_id_from_url(url)
        assert realm == "dicorp.quickbase.com"
        assert app_id == "bqx7xre7a"


class TestNormalizeUnicode:
    def test_all_ascii_is_same(self):
        assert normalize_unicode("foo") == "foo"

    def test_normalizes_if_accent(self):
        assert normalize_unicode("Carlos Pe\u00F1a") == "Carlos Pena"
