import pytest

from quickbase_client.tools import qbc
from quickbase_client.tools.script import Script
from quickbase_client.tools.script_loader import ScriptManager


@pytest.fixture()
def example_script(monkeypatch):
    class MyScript(Script):
        registration_name = "foo"

        def __init__(self, flag):
            self.flag = flag

        def run(self):
            if self.flag:
                raise SyntaxError("lol")
            return 5

        @staticmethod
        def add_argparse_args(parser):
            parser.add_argument("--flag", action="store_true")
            parser.add_argument("--blah", nargs="?", required=True)

        @staticmethod
        def instantiate_from_ns(ns) -> "Script":
            return MyScript(ns.flag)

    mgr = ScriptManager()
    mgr.register_script(MyScript)
    new_scripts = mgr
    monkeypatch.setattr(qbc, "scripts", new_scripts)

    return MyScript


class TestQbcModelGenerator:
    def test_parse_ok(self, example_script):
        x = qbc.main(["run", "foo", "--blah", "bleh"])
        assert x == 5

    def test_requires_subparse_arg(self, example_script):
        with pytest.raises(SystemExit):
            qbc.main(["run", "foo"])

    def test_catches_script_exception(self, example_script):
        with pytest.raises(SystemExit):
            qbc.main(["run", "foo", "--blah", "bleh", "--flag"])

    def test_re_raises_if_stacktrace_on(self, example_script):
        with pytest.raises(SyntaxError):
            qbc.main(["--show-stacktrace", "run", "foo", "--blah", "bleh", "--flag"])

    def test_unregistered_script(self, example_script):
        with pytest.raises(SystemExit):
            qbc.main(["run", "bar", "--blah", "bleh"])
