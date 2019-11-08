from MicroCompiler.lexer.tokens import Token


class Terminal:
    def __init__(self, name: str):
        self.name = name

        # TODO: this is a little hack for store token info
        self.token = None  # type: Token

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
