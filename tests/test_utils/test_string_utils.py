from quickbase_client.utils.string_utils import make_var_name


class TestMakeVarName:

    def test_no_preceding_numbers(self):
        v = make_var_name('1abc')
        assert '1' not in v
        assert v == 'abc'

    def test_use_underscore_before_numbers(self):
        v = make_var_name('1bc', number_strategy='underscore')
        assert v == '_1bc'

    def test_no_special_chars(self):
        v = make_var_name('abc-123')
        assert '-' not in v

    def test_snake_case_special_char_to_underscore(self):
        v = make_var_name('abc - 123')
        assert v == 'abc_123'

    def test_pascal_case_drops_special_chars(self):
        v = make_var_name('abc - 123', case='pascal')
        assert v == 'Abc123'

    def test_snake_case(self):
        v = make_var_name('abc def')
        assert v == 'abc_def'

    def test_snake_all_caps(self):
        v = make_var_name('ABC')
        assert v == 'abc'
