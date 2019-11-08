from MicroCompiler.LR.lr_one_item import LR1Item
from MicroCompiler.LR.rhs import RightHandSide
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import Terminal


def test_eq():
    lr_1_item = LR1Item("S", RightHandSide(["S", "E"], placeholder_offset=1), "a")

    new_lr_1_item = LR1Item("S", RightHandSide(["S", "E"], placeholder_offset=1), "a")

    assert new_lr_1_item == lr_1_item


def test_str():
    lr_1_item = LR1Item(
        "S",
        RightHandSide([NonTerminal("S"), Terminal("type", "e")], placeholder_offset=1),
        "a",
    )
    lr_1_str = str(lr_1_item)

    assert lr_1_str == "[S ⭢ S • 'e', a]"


def test_repr():
    lr_1_item = LR1Item(
        "S",
        RightHandSide([NonTerminal("S"), Terminal("type", "e")], placeholder_offset=1),
        "a",
    )
    lr_1_repr = repr(lr_1_item)

    # TODO
