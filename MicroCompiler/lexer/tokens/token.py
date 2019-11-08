from MicroCompiler.lexer.tokens.base_token import BaseToken


class Token(BaseToken):
    def __str__(self):
        if self.value is None:
            return "Token({!r})".format(self.type)

        return "Token({!r}: {!r})".format(self.type, self.value)

    def __repr__(self):
        return "{}({!r}, value={!r})".format(self.__class__.__name__, self.type, self.value)
