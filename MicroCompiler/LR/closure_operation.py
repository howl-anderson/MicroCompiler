import copy
from typing import Set, FrozenSet

from MicroCompiler.LR.state import State
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.FirstSet import FirstSet
from MicroCompiler.Productions import Productions
from MicroCompiler.LR.lr_one_item import LR1Item
from MicroCompiler.LR.rhs import RightHandSide
from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.Lookahead.NonTerminal import NonTerminal


def closure_operation(
    items: Set[LR1Item], productions: Productions, first_set
) -> State:
    while True:
        new_items = copy.deepcopy(items)

        for item in items:
            next_symbol = item.rhs.get_symbol_around_mark(offset=1)
            if next_symbol is None or isinstance(next_symbol, Terminal):
                continue

            lookahead_candidate = item.rhs.get_symbols_around_mask_to_tail()
            lookahead_candidate.append(item.lookahead)

            lookahead = first_set.get_first_set(lookahead_candidate)

            production_group = productions.get(next_symbol)
            for production_branch in production_group:
                for first_set_item in lookahead:
                    new_lr_one_item = LR1Item(
                        lhs=next_symbol,
                        rhs=RightHandSide(production_branch, 0),
                        lookahead=first_set_item,
                    )

                    if new_lr_one_item not in new_items:
                        new_items.add(new_lr_one_item)

        if frozenset(new_items) == frozenset(items):
            break
        else:
            items = new_items

    return State(items)


if __name__ == "__main__":
    # Goal -> . SheepNoise , EOF
    lr_1_item = {
        LR1Item(
            NonTerminal("Goal"), RightHandSide([NonTerminal("SheepNoise")], 0), EOF()
        )
    }

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
