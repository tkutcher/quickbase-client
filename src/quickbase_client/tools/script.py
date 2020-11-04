import abc


class Script(abc.ABC):
    registration_name = None

    @abc.abstractmethod
    def run(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def add_argparse_args(parser):
        pass

    @staticmethod
    @abc.abstractmethod
    def instantiate_from_ns(ns) -> 'Script':
        pass
