from quickbase_client import QuickBaseField
from quickbase_client import QuickBaseFieldType


class TestQuickBaseField:

    def test_is_formula_false(self):
        f = QuickBaseField(fid=7, field_type=QuickBaseFieldType.TEXT, formula='[Other field]')
        assert f.is_formula

    def test_is_formula_true(self):
        f = QuickBaseField(fid=7, field_type=QuickBaseFieldType.TEXT)
        assert not f.is_formula
