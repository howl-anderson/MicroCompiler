from MicroCompiler.cfg.symbol import Symbol


class Epsilon(Symbol):
    def __str__(self):
        return "ϵ"

    @property
    def value(self):
        return "ϵ"

    def __hash__(self):
        return hash("ϵ")

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return True

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)
