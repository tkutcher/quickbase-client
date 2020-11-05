import pytest

from quickbase_client.tools.model_generate import ModelGenerator
from quickbase_client.tools.script import Script
from quickbase_client.tools.script_loader import CoreScriptLoader
from quickbase_client.tools.script_loader import ScriptManager


class TestScriptManager:

    def test_add_script(self):
        class MyScript(Script):
            registration_name = 'myscript'

            def run(self):
                pass

            @staticmethod
            def add_argparse_args(parser):
                pass

            @staticmethod
            def instantiate_from_ns(ns) -> 'Script':
                return MyScript()

        mgr = ScriptManager()
        mgr.register_script(MyScript)
        assert mgr.get_script_by_name('myscript') is MyScript


class TestCoreScriptLoader:

    @pytest.mark.parametrize('script_cls', [
        ModelGenerator
    ])
    def test_loads_script(self, script_cls):
        mgr = CoreScriptLoader().load_scripts()
        assert mgr.get_script_by_name(script_cls.registration_name) is script_cls
