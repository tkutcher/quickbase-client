import os
from tempfile import TemporaryDirectory

import pytest
from quickbase_client.tools import model_generate
from quickbase_client.tools.model_generate import ModelGenerator


@pytest.fixture()
def run_generator(qb_api_mock, monkeypatch):
    def _post_run_generator(f=lambda d: None):
        with TemporaryDirectory() as d:
            monkeypatch.setattr(model_generate.os, 'getcwd', lambda: d)
            gen = ModelGenerator(realm_hostname='example.quickbase.com', user_token='foo',
                                 app_id='abcdef', pkg_dir=d)
            gen.run()
            f(d)
        return gen
    return _post_run_generator


class TestModelGenerator:

    def test_write_to_models_dir_from_cwd_by_default(self, qb_api_mock, monkeypatch):
        with TemporaryDirectory() as d:
            monkeypatch.setattr(model_generate.os, 'getcwd', lambda: d)
            gen = ModelGenerator(realm_hostname='example.quickbase.com', user_token='foo',
                                 app_id='abcdef')
            gen.run()
            assert os.path.exists(os.path.join(d, 'models'))
            assert os.path.exists(os.path.join(d, 'models', '__init__.py'))

    def test_makes_package_by_name_from_parent_dir(self, run_generator):
        def _asserts(d):
            assert os.path.exists(os.path.join(d, 'qbcpy'))
            assert os.path.exists(os.path.join(d, 'qbcpy', '__init__.py'))
        run_generator(_asserts)

    def test_makes_app_file(self, run_generator):
        def _asserts(d):
            assert os.path.exists(os.path.join(d, 'qbcpy', 'app.py'))
        run_generator(_asserts)

    def test_app_file_has_version(self, run_generator):
        gen = run_generator()
        app_module = gen.pkg_writer.modules['app']
        s = app_module.get_file_as_string()
        assert '__versionid__ = ' in s
        assert '20201103042209Z' in s

    def test_app_file_creates_var(self, run_generator):
        gen = run_generator()
        app_module = gen.pkg_writer.modules['app']
        s = app_module.get_file_as_string()
        assert 'Qbcpy = QuickBaseApp(' in s
