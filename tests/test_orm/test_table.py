from datetime import date

import pytest

from quickbase_client.orm.field import QuickBaseFieldType as Qb


class TestQuickBaseTable:

    def test_can_create_record_objects(self, example_table):
        rec = example_table(
            field_1='A',
            field_2=['A', 'B'],
            field_3=99.2,
            field_4=date(year=2020, month=10, day=28))
        assert rec.field_1 == 'A'
        assert rec.field_2 == ['A', 'B']
        assert rec.field_3 == 99.2
        assert rec.field_4 == date(year=2020, month=10, day=28)

    def test_not_all_required(self, example_table):
        rec = example_table(field_1='A')
        assert rec.field_1 == 'A'
        assert rec.field_2 is None
        assert rec.field_3 is None
        assert rec.field_4 is None

    def test_cannot_set_unspecified_attributes(self, example_table):
        with pytest.raises(AttributeError) as e:
            _ = example_table(this_does_not_exist='hello')
            assert 'this_does_not_exist' in str(e)

    def test_get_field_info(self, example_table):
        field_info = example_table.get_field_info('field_1')
        assert field_info.field_type == Qb.TEXT
