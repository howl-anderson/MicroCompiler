# Used to replace MicroCompiler.Lookahead.NonTerminal.NonTerminal


class NonTerminal:
    def __init__(self, name):
        self.name = name

        super().__init__()

    @property
    def value(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.name)

    def __deepcopy__(self, memodict={}):
        return self.__class__(self.name)
