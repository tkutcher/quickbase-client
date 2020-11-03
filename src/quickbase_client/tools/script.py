import abc


class Script(abc.ABC):

    @abc.abstractmethod
    def run(self):
        pass
