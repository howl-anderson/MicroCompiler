from .Epsilon import Epsilon


class SymbolSet(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def include_epsilon(self):
        return any([i for i in self if isinstance(i, Epsilon)])

    def remove_epsilon(self):
        return self.__class__({i for i in self if not isinstance(i, Epsilon)})
