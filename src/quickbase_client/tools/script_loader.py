import abc
from typing import Type

from quickbase_client.tools.model_generate import ModelGenerator
from quickbase_client.tools.script import Script


class ScriptManager(object):
    def __init__(self):
        self.scripts = {}

    def all_scripts(self):
        return self.scripts.keys()

    def register_script(self, script_cls: Type[Script]):
        name = script_cls.registration_name
        if name in self.scripts:
            raise KeyError(f'Script {name} already registered!')
        self.scripts[name] = script_cls

    def get_script_by_name(self, name):
        return self.scripts[name]


class ScriptLoader(abc.ABC):

    @abc.abstractmethod
    def load_scripts(self) -> ScriptManager:
        pass


class CoreScriptLoader(ScriptLoader):

    def load_scripts(self):
        mgr = ScriptManager()
        mgr.register_script(ModelGenerator)
        return mgr
