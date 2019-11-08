from MicroCompiler.cfg.symbol import Symbol
from MicroCompiler.lexer.tokens import Token

CHARACTER = "CHARACTER"


class Terminal(Symbol):
    def __init__(self, type: str):
        self.type = type

        # TODO: this is a little hack for store token info
        self.token = None  # type: Token

        super().__init__()

    @property
    def value(self):
        return str(self.type)

    @classmethod
    def convert_from_token(cls, token: Token):
        self = cls(token.type)
        self.token = token

        return self

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.type == other.type

    def __hash__(self):
        return hash(self.type)

    def __str__(self):
        return "'{}'".format(self.type)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.type)
