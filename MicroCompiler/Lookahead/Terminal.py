from MicroCompiler.Lookahead.symbol import Symbol
from MicroRegEx.Token import Token

CHARACTER = "CHARACTER"


class Terminal(Symbol):
    def __init__(self, type_=None, data=None):
        if type_ is None:
            type_ = CHARACTER
        self.type_ = type_

        if data is None:
            raise ValueError("value can not be None")
        self.data = data

        # TODO: this is a little hack for store token info
        self.token = None  # type: Token

        super().__init__()

    @property
    def value(self):
        return str(self.data)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.type_ == other.type_ and self.data == other.data:
            return True
        return False

    def __hash__(self):
        return hash((self.type_, self.data))

    def __str__(self):
        return "'{}'".format(self.data)

    def __repr__(self):
        return "{}({}, '{}')".format(self.__class__.__name__, self.type_, self.data)
