from .singleton_meta import SingletonMeta


class ProgramControl(metaclass=SingletonMeta):

    def __init__(self):
        self._exit = False

    def exit(self):
        self._exit = True

    @property
    def is_exit(self) -> bool:
        return self._exit
