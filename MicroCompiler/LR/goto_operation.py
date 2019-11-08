import copy
from typing import Set, Union, FrozenSet

from MicroCompiler.LR.lr_one_item import LR1Item
from MicroCompiler.LR.closure_operation import closure_operation
from MicroCompiler.LR.rhs import RightHandSide
from MicroCompiler.LR.state import State
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.FirstSet import FirstSet
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.Productions import Productions


def goto_operation(
    state: State,
    symbol: Union[Terminal, NonTerminal],
    productions: Productions,
    first_set: FirstSet,
) -> State:
    new_items = set()

    filtered_state = list(
        filter(lambda x: x.rhs.get_symbol_around_mark(offset=1) == symbol, state)
    )

    for item in filtered_state:
        new_item = copy.deepcopy(item)
        new_item.rhs.forward_mask()

        if new_item not in new_items:
            new_items.add(new_item)

    return closure_operation(new_items, productions, first_set)


if __name__ == "__main__":
    # Goal -> . SheepNoise , EOF
    lr_1_item = [
        LR1Item(
            NonTerminal("Goal"), RightHandSide([NonTerminal("SheepNoise")], 0), EOF()
        )
    ]

    productions = Productions(
        {
            # Goal -> SheepNoise
            NonTerminal("Goal"): [[NonTerminal("SheepNoise")]],
            # SheepNoise -> SheepNoise baa
            #             | baa
            NonTerminal("SheepNoise"): [
                [NonTerminal("SheepNoise"), Terminal("sound", "baa")],
                [Terminal("sound", "baa")],
            ],
        }
    )

    first_set = FirstSet(productions)
    first_set.compute()

    closure_items = closure_operation(lr_1_item, productions, first_set)
    print(closure_items)

    new_closure_items = goto_operation(
        closure_items, Terminal("sound", "baa"), productions, first_set
    )
    print(new_closure_items)
