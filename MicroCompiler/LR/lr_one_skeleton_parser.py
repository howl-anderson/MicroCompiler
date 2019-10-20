from typing import Tuple, List

from MicroCompiler.LR.canonical_collectoin_builder import canonical_collection_builder
from MicroCompiler.LR.lr_one_item import LR1Item
from MicroCompiler.LR.rhs import RightHandSide
from MicroCompiler.LR.state import State
from MicroCompiler.LR.table_construction_builder import (
    Reduce,
    Shift,
    Accept,
    table_construction_builder,
)
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.FirstSet import FirstSet
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.Productions import Productions


class Stack(List[Tuple[str, State]]):
    def push(self, i):
        self.append(i)

    def get_top(self):
        return self[-1]

    def pop_top_k(self, k: int):
        for _ in range(k):
            self.pop()


class Lexer(List[Terminal]):
    def __init__(self, *args, **kwargs):
        self.current_offset = 0
        super().__init__(*args, **kwargs)

    def get_next(self) -> Terminal:
        if self.current_offset >= len(self):
            raise ValueError()

        token = self[self.current_offset]
        self.current_offset += 1

        return token


class ParserError(Exception):
    pass


def lr_one_skeleton_parser(lexer, states, action_table, goto_table):
    stack = Stack()

    stack.push(None)
    stack.push(("Goal", states.get_state_zero()))

    word = lexer.get_next()

    while True:
        _, state = stack.get_top()
        action = action_table.get((state, word))
        if isinstance(action, Reduce):
            stack.pop_top_k(len(action.rhs))

            _, state = stack.get_top()
            goto_state = goto_table.get((state, action.lhs))

            stack.push((action.lhs, goto_state))

            print(action)
        elif isinstance(action, Shift):
            stack.push((word, action.next_state))

            word = lexer.get_next()

        elif isinstance(action, Accept) and word == EOF():
            break

        else:
            raise ParserError()


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

    lexer = Lexer([Terminal("baa", "baa"), Terminal("baa", "baa"), EOF()])

    lr_one_skeleton_parser(lexer, states, action, goto_table)
