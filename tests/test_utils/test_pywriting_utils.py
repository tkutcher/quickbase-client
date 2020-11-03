import os
from tempfile import TemporaryDirectory

from quickbase_client.utils.pywriting_utils import BasicPyFileWriter
from quickbase_client.utils.pywriting_utils import PyPackageWriter


class TestBasicFileWriter:

    def test_outputs_lines(self):
        w = BasicPyFileWriter()
        w.add_line('import abc')
        w.add_line('import os')
        s = w.get_file_as_string()
        assert s == 'import abc\nimport os\n'


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
