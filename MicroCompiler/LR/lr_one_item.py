import copy

from MicroCompiler.LR.rhs import RightHandSide
from MicroCompiler.Lookahead import NonTerminal


class LR1Item(object):
    def __init__(self, lhs: NonTerminal, rhs: RightHandSide, lookahead):
        self.lhs = lhs
        self.rhs = rhs  # type: RightHandSide
        self.lookahead = lookahead

        self.arrow_symbol = "⭢"

    def __str__(self):
        return "[{} {} {}, {}]".format(self.lhs, self.arrow_symbol, self.rhs, self.lookahead)

    # def __repr__(self):
    #     return "{!s} -> {!s} , {!s}".format(self.lhs, self.rhs, self.lookahead)

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(
            self.__class__.__name__, self.lhs, self.rhs, self.lookahead
        )

    def __hash__(self):
        return hash((self.lhs, self.rhs, self.lookahead))

    def __eq__(self, other):
        return (
            self.lhs == other.lhs
            and self.rhs == other.rhs
            and self.lookahead == other.lookahead
        )

    def __deepcopy__(self, memodict={}):
        return self.__class__(
            lhs=copy.deepcopy(self.lhs),
            rhs=copy.deepcopy(self.rhs),
            lookahead=copy.deepcopy(self.lookahead),
        )


if __name__ == "__main__":
    lr_1_item = LR1Item("S", RightHandSide(["S", "E"], placeholder_offset=1), "a")
    lr_1_str = str(lr_1_item)
    print(lr_1_str)

    lr_1_repr = repr(lr_1_item)
    print(lr_1_repr)

    new_lr_1_item = LR1Item("S", RightHandSide(["S", "E"], placeholder_offset=1), "a")

    assert new_lr_1_item == lr_1_item
