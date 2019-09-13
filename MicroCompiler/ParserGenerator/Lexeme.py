NON_TERMINAL = "NON_TERMINAL"
TERMINAL = "TERMINAL"
PRODUCT = "PRODUCT"
SEMICOLON = "SEMICOLON"
ALTERNATIVE = "ALTERNATIVE"
EPSILON = "EPSILON"


class Lexeme:
    def __init__(self, type_, value):
        self.value = value
        self.type_ = type_

    def __repr__(self):
        return "{}({}, '{}')".format(self.__class__.__name__, self.type_, self.value)

    def __str__(self):
        return "<{}: {}>".format(self.type_, self.value)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.type_ == other.type_ and self.value == other.value:
            return True
        return False

    def __hash__(self):
        return hash(frozenset({self.value, self.type_}))
