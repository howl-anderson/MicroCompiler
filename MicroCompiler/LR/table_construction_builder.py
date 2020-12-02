from typing import Set, FrozenSet, Union, Tuple

from MicroCompiler.LR.canonical_collectoin_builder import canonical_collection_builder
from MicroCompiler.LR.goto_operation import goto_operation
from MicroCompiler.LR.lr_one_item import LR1Item
from MicroCompiler.LR.rhs import RightHandSide
from MicroCompiler.LR.state import State
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.FirstSet import FirstSet
from MicroCompiler.cfg import NonTerminal, Epsilon
from MicroCompiler.cfg import Terminal
from MicroCompiler.Productions import Productions


class ShiftReduceConflict(Exception):
    pass


class ReduceReduceConflict(Exception):
    pass


class ActionTable(dict):
    def add_action(
        self,
        condition: Tuple[State, Union[NonTerminal, Terminal, EOF]],
        action: "ParserAction",
    ):
        if isinstance(condition[1], Epsilon):
            print("")

        if condition not in self:
            self[condition] = action
        else:
            existed_action = self[condition]

            if existed_action == action:
                # do nothing
                return

            if isinstance(action, Shift) and isinstance(existed_action, Reduce):
                raise ShiftReduceConflict(str(action), str(existed_action), str(condition))
            elif isinstance(action, Reduce) and isinstance(existed_action, Shift):
                raise ShiftReduceConflict(str(action), str(existed_action), str(condition))
            elif isinstance(action, Reduce) and isinstance(existed_action, Reduce):
                raise ReduceReduceConflict(str(action), str(existed_action), str(condition))
            else:
                raise ValueError()

    def filter_by_state(self, state):
        filtered_state = dict()
        for k, v in self.items():
            s, t = k
            if s == state:
                filtered_state[k] = v

        return filtered_state


class ParserAction(object):
    pass


class Shift(ParserAction):
    def __init__(self, next_state):
        self.next_state = next_state

    def __str__(self):
        return "{!s} {!s}".format(self.__class__.__name__, self.next_state)

    def __repr__(self):
        return "{!s}({!r})".format(self.__class__.__name__, self.next_state)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.next_state == other.next_state


class Accept(ParserAction):
    def __repr__(self):
        return "{}".format(self.__class__.__name__)


class Reduce(ParserAction):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "{!s} {!s} -> {!s}".format(self.__class__.__name__, self.lhs, self.rhs)

    def __repr__(self):
        return "{!s}({!r}, {!r})".format(self.__class__.__name__, self.lhs, self.rhs)


def table_construction_builder(states: Set[State], productions, first_set, end_point):
    action_table = ActionTable()
    goto_table = {}

    for state in states:
        for item in state:
            # next symbol around mark
            symbol = item.rhs.get_symbol_around_mark(offset=1)
            # next_state = goto_table.get((state, symbol))
            next_state = goto_operation(state, symbol, productions, first_set)
            if isinstance(symbol, Terminal) and next_state:
                next_state.setup_id()
                action_table.add_action((state, symbol), Shift(next_state))
            elif item == end_point:
                action_table.add_action((state, EOF()), Accept())
            elif item.rhs.is_mark_at_end():
                # # SomeNonTerminal -> Epsilon is special case
                # if len(item.rhs) == 0:
                #     # skip this item
                #     continue

                action_table.add_action(
                    (state, item.lookahead), Reduce(item.lhs, item.rhs)
                )

        for non_terminal in productions.get_all_non_terminals():
            # next_state = goto_table.get((state, non_terminal))
            next_state = goto_operation(state, non_terminal, productions, first_set)
            if next_state:
                next_state.setup_id()
                goto_table[(state, non_terminal)] = next_state

    return action_table, goto_table


if __name__ == "__main__":
    end_point = LR1Item(
        NonTerminal("Goal"), RightHandSide([NonTerminal("SheepNoise")], 1), EOF()
    )

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

    action, goto_table = table_construction_builder(
        states, productions, first_set, end_point
    )
    print(action, goto_table)
