from datetime import date

import pytest
from quickbase_client.orm.field import QuickBaseField
from quickbase_client.orm.field import QuickBaseFieldType as Qb
from quickbase_client.query.ast import eq_
from quickbase_client.query.ast import qb_query_ast
from quickbase_client.query.query_base import QuickBaseQuery
from quickbase_client.query import ast


mock_field = QuickBaseField(fid=18, field_type=Qb.TEXT)
mock_field_2 = QuickBaseField(fid=19, field_type=Qb.DATE)


class TestAstQueryBuilding:

    def test_decorator_wraps_in_obj(self):
        @qb_query_ast
        def foo():
            return "{'18'.EX.19}"
        x = foo()
        assert isinstance(x, QuickBaseQuery)
        assert x.where == "{'18'.EX.19}"

    def test_makes_string(self):
        q = eq_(mock_field, 19)
        assert q.where == "{'18'.EX.19}"

    def test_simple_conjunction(self):
        q = ast.and_(
            ast.eq_(mock_field, 19),
            ast.on_or_before_(mock_field_2, date(year=2020, day=7, month=2)))
        assert "{'18'.EX.19}AND{'19'.OBF.'02-07-2020'}" in q.where

    def test_combine_conjunctions(self):
        q = ast.and_(
            ast.or_(
                ast.eq_(mock_field, 19),
                ast.eq_(mock_field, 21)),
            ast.on_or_before_(mock_field_2, date(year=2020, day=7, month=2)))
        assert q.where == "(({'18'.EX.19}OR{'18'.EX.21})AND{'19'.OBF.'02-07-2020'})"

    @pytest.mark.parametrize('f,op', [
        ('contains_', 'CT'), ('not_contains_', 'XCT'),
        ('has_', 'HAS'), ('not_has_', 'XHAS'),
        ('eq_', 'EX'), ('not_eq_', 'XEX'),
        ('true_', 'TV'),
        ('starts_with_', 'SW'), ('not_starts_width_', 'XSW'),
        ('before_', 'BF'), ('on_or_before_', 'OBF'),
        ('after_', 'AF'), ('on_or_after_', 'OAF'),
        ('during_', 'IR'), ('not_during_', 'XIR'),
        ('lt_', 'LT'), ('lte_', 'LTE'),
        ('gt_', 'GT'), ('gte_', 'GTE')])
    def test_all(self, f, op):
        f = getattr(ast, f)
        q = f(mock_field, 'oops')
        assert q.where == f"{{'18'.{op}.'oops'}}"
