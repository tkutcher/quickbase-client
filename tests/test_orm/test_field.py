from quickbase_client import QuickbaseField
from quickbase_client import QuickbaseFieldType


class TestQuickBaseField:
    def test_is_formula_false(self):
        f = QuickbaseField(
            fid=7, field_type=QuickbaseFieldType.TEXT, formula="[Other field]"
        )
        assert f.is_formula

    def test_is_formula_true(self):
        f = QuickbaseField(fid=7, field_type=QuickbaseFieldType.TEXT)
        assert not f.is_formula
