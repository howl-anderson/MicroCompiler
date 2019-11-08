from MicroCompiler.lexer.tokens.base_token import BaseToken


class WhiteSpaceToken(BaseToken):
    def __init__(self, value=None):
        super(WhiteSpaceToken, self).__init__('WHITE_SPACE', value=value)

    def __str__(self):
        return "WhiteSpaceToken({!r})".format(self.value)

    def __repr__(self):
        return "{}({!r}, value={!r})".format(self.__class__.__name__, self.type, self.value)