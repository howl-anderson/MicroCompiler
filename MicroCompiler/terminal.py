# Used to replace MicroCompiler.Lookahead.Terminal.Terminal


class Terminal:
    def __init__(self, name):
        self.name = name

        super().__init__()

    @property
    def value(self):
        return str(self.name)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "'{}'".format(self.name)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.name)

    def __deepcopy__(self, memodict={}):
        return self.__class__(self.name)
