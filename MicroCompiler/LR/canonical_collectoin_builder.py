import copy
from typing import Set, FrozenSet, Union

from MicroCompiler.LR.closure_operation import closure_operation
from MicroCompiler.LR.goto_operation import goto_operation
from MicroCompiler.LR.lr_one_item import LR1Item
from MicroCompiler.LR.rhs import RightHandSide
from MicroCompiler.LR.state import State
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.FirstSet import FirstSet
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.Productions import Productions
from micro_toolkit.cache.cache_me import cache_me

goto_table = {}


class StateSet(Set[State]):
    def get_state_zero(self):
        for i in self:
            if i.id == 0:
                return i


def record(
    src: FrozenSet[LR1Item], dst: FrozenSet[LR1Item], on: Union[Terminal, NonTerminal]
):
    goto_table[(src, on)] = dst


# @cache_me()
def canonical_collection_builder(
    start_point: Set[LR1Item], productions: Productions, first_set: FirstSet
) -> StateSet:
    state_zero = closure_operation(start_point, productions, first_set)
    state_zero.setup_id()
    states = StateSet()
    states.add(state_zero)

    while True:
        new_states = copy.deepcopy(states)
        for state in states:
            for symbol in productions.get_all_elements():
                new_state = goto_operation(state, symbol, productions, first_set)

                if not new_state:  # empty frozenset
                    continue

                if new_state not in new_states:
                    new_state.setup_id()

                    record(src=state, dst=new_state, on=symbol)

                    new_states.add(new_state)

        if frozenset(new_states) == frozenset(states):
            break
        else:
            states = new_states

    return new_states


if __name__ == "__main__":
    start_point = {
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
                [NonTerminal("SheepNoise"), Terminal("baa", "baa")],
                [Terminal("baa", "baa")],
            ],
        }
    )
    productions.set_start_symbol(NonTerminal("Goal"))

    first_set = FirstSet(productions)
    first_set.compute()

    states = canonical_collection_builder(start_point, productions, first_set)

    print(states)
