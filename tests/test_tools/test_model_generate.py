import os
from tempfile import TemporaryDirectory

import pytest
from requests import Response

from quickbase_client.tools import model_generate
from quickbase_client.tools import qbc
from quickbase_client.tools.model_generate import ModelGenerator


@pytest.fixture()
def run_generator(qb_api_mock, monkeypatch):
    def _post_run_generator(f=lambda d, run_result: None, **kwargs: None):
        with TemporaryDirectory() as d:
            monkeypatch.setattr(model_generate.os, 'getcwd', lambda: d)
            gen = ModelGenerator(realm_hostname='example.quickbase.com', app_id='abcdef',
                                 user_token='foo', pkg_dir=d, **kwargs)
            run_result = gen.run()
            f(d, run_result)
        return gen
    return _post_run_generator


class TestModelGenerator:

    def test_write_to_models_dir_from_cwd_by_default(self, qb_api_mock, monkeypatch):
        with TemporaryDirectory() as d:
            monkeypatch.setattr(model_generate.os, 'getcwd', lambda: d)
            gen = ModelGenerator(realm_hostname='example.quickbase.com', app_id='abcdef',
                                 user_token='foo')
            gen.run()
            assert os.path.exists(os.path.join(d, 'models'))
            assert os.path.exists(os.path.join(d, 'models', '__init__.py'))

    def test_makes_package_by_name_from_parent_dir(self, run_generator):
        def _asserts(d, _):
            assert os.path.exists(os.path.join(d, 'qbcpy'))
            assert os.path.exists(os.path.join(d, 'qbcpy', '__init__.py'))
        run_generator(_asserts)

    def test_makes_app_file(self, run_generator):
        def _asserts(d, _):
            assert os.path.exists(os.path.join(d, 'qbcpy', 'app.py'))
        run_generator(_asserts)

    def test_app_file_has_version(self, run_generator):
        gen = run_generator()
        app_module = gen.pkg_writer.modules['app']
        s = app_module.get_file_as_string()
        assert '__versionid__ = ' in s
        assert '20201103042209' in s

    def test_app_file_creates_var(self, run_generator):
        gen = run_generator()
        app_module = gen.pkg_writer.modules['app']
        s = app_module.get_file_as_string()
        assert 'Qbcpy = QuickBaseApp(' in s

    def test_creates_table_files(self, run_generator):
        def _asserts(d, _):
            assert os.path.exists(os.path.join(d, 'qbcpy', 'debug.py'))
            assert os.path.exists(os.path.join(d, 'qbcpy', 'idea.py'))
            assert os.path.exists(os.path.join(d, 'qbcpy', 'ideas_2.py'))
        run_generator(_asserts)

    def test_creates_only_requested_table_files(self, run_generator):
        def _asserts(d, _):
            assert not os.path.exists(os.path.join(d, 'qbcpy', 'debug.py'))
            assert os.path.exists(os.path.join(d, 'qbcpy', 'idea.py'))
            assert os.path.exists(os.path.join(d, 'qbcpy', 'ideas_2.py'))
        run_generator(_asserts, table_ids=['idea', 'cccccc'])

    def test_writes_table_class(self, run_generator):
        gen = run_generator()
        m = gen.pkg_writer.modules['debug']
        s = m.get_file_as_string()
        assert 'QuickBaseTable):' in s
        assert 'class' in s
        assert 'field_type=' in s

    def test_good_var_names(self, run_generator):
        gen = run_generator()
        m = gen.pkg_writer.modules['debug']
        s = m.get_file_as_string()
        assert 'def_' in s
        assert 'funky_label' in s and '_funky' not in s
        assert 'some_basic_text_field' in s

    def test_clashing_table_names(self, run_generator):
        gen = run_generator()
        assert 'idea' in gen.pkg_writer.modules
        assert 'ideas_2' in gen.pkg_writer.modules

    def test_formulas_added(self, run_generator):
        gen = run_generator()
        m = gen.pkg_writer.modules['idea']
        s = m.get_file_as_string()
        assert "'''var text desc = [Description]" in s
        assert "$desc'''" in s
        assert 'formula=' in s

    def test_script_args(self, monkeypatch, run_generator):
        def _intercept_run(self_):
            return self_
        monkeypatch.setattr(ModelGenerator, 'run', _intercept_run)

        with TemporaryDirectory() as d:
            monkeypatch.setattr(model_generate.os, 'getcwd', lambda: d)
            c = qbc.main(['run', 'model-generate', '--app-url',
                          'https://example.quickbase.com/db/abcdef', '-t', 'whocares'])
            assert c.realm_hostname == 'example.quickbase.com'
            assert c.app_id == 'abcdef'
            assert c.user_token == 'whocares'
            assert c.table_ids == []

    def test_script_args_accepts_table_ids(self, monkeypatch):
        def _intercept_run(self_):
            return self_
        monkeypatch.setattr(ModelGenerator, 'run', _intercept_run)

        with TemporaryDirectory() as d:
            monkeypatch.setattr(model_generate.os, 'getcwd', lambda: d)
            c = qbc.main(['run', 'model-generate', '--app-url',
                          'https://example.quickbase.com/db/abcdef', '-t', 'whocares',
                          '-i', 'table123', '--include', 'bx123sdf'])
            assert c.realm_hostname == 'example.quickbase.com'
            assert c.app_id == 'abcdef'
            assert 'table123' in c.table_ids
            assert 'bx123sdf' in c.table_ids
            assert len(c.table_ids) == 2

    def test_loads_token_from_environment(self, monkeypatch):
        monkeypatch.setenv('QB_USER_TOKEN', 'foo')

        def _intercept_run(self_):
            return self_
        monkeypatch.setattr(ModelGenerator, 'run', _intercept_run)

        with TemporaryDirectory() as d:
            monkeypatch.setattr(model_generate.os, 'getcwd', lambda: d)
            c = qbc.main(['run', 'model-generate', '--app-url',
                          'https://example.quickbase.com/db/abcdef'])
            assert c.user_token == 'foo'

    def test_error_if_no_token_anywhere(self, monkeypatch):
        monkeypatch.delenv('QB_USER_TOKEN', raising=False)

        def _intercept_run(self_):
            return self_
        monkeypatch.setattr(ModelGenerator, 'run', _intercept_run)

        with TemporaryDirectory() as d:
            monkeypatch.setattr(model_generate.os, 'getcwd', lambda: d)
            with pytest.raises(SystemExit):
                qbc.main(['run', 'model-generate', '--app-url',
                          'https://example.quickbase.com/db/abcdef'])

    def test_uses_table_instead_of_app_url_error(self, run_generator, monkeypatch):
        r = Response()
        r.status_code = 400
        r._content = b'{"message": "Invalid DBID"}'

        def _asserts(d, run_result):
            assert not run_result
        monkeypatch.setattr(model_generate.QuickBaseApiClient, 'get_app', lambda _1, _2: r)
        run_generator(_asserts)

    def test_other_bad_api_call(self, run_generator, monkeypatch):
        r = Response()
        r.status_code = 400
        r._content = b'{"message": "some other issue"}'
        monkeypatch.setattr(model_generate.QuickBaseApiClient, 'get_app', lambda _1, _2: r)

        with pytest.raises(ValueError):
            run_generator()
