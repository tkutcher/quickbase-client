import os
from tempfile import TemporaryDirectory

from quickbase_client.utils.pywriting_utils import BasicPyFileWriter
from quickbase_client.utils.pywriting_utils import PyPackageWriter


class TestBasicFileWriter:

    def test_outputs_lines(self):
        w = BasicPyFileWriter()
        w.add_line('import abc')
        w.add_line('import os').space()
        s = w.get_file_as_string()
        assert s == 'import abc\nimport os\n'

    def test_indent_dedent(self):
        w = BasicPyFileWriter()
        w.add_line('def foo():').indent().add_line('return 5').dedent().space()
        s = w.get_file_as_string()
        assert s == 'def foo():\n    return 5\n'

    def test_use_refs(self):
        w = BasicPyFileWriter()
        w.add_line('a = "A"')
        ref = w.make_ref()
        w.add_line('d = "D"')
        ref.add_line('b = "B"').add_line('c = "C"')
        s = w.get_file_as_string()
        lns = s.split('\n')
        assert 'a' in lns[0]
        assert 'b' in lns[1]
        assert 'c' in lns[2]
        assert 'd' in lns[3]


class TestPyPackageWriter:

    def test_includes_init(self):
        with TemporaryDirectory() as d:
            w = PyPackageWriter(pkg_name='foo', parent_dir=d)
            assert '__init__' in w.modules
            assert w.has_module_name('__init__')
            assert w.pkg_path == os.path.join(d, 'foo')
            w.write()
            assert os.path.exists(d)
            assert os.path.exists(os.path.join(d, 'foo'))
            assert os.path.exists(os.path.join(d, 'foo', '__init__.py'))
