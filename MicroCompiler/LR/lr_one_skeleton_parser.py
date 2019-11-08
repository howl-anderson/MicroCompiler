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
from MicroCompiler.ast import Instance
from MicroCompiler.cfg import NonTerminal
from MicroCompiler.cfg import Terminal
from MicroCompiler.Productions import Productions
from MicroCompiler.ast.ast import AST_v2
from MicroCompiler.lexer import Lexer
from MicroCompiler.lexer.tokens import Token


class Stack(List[Tuple[str, State]]):
    def push(self, i):
        self.append(i)

    def get_top(self):
        return self[-1]

    def pop_top_k(self, k: int):
        top_k = []

        for _ in range(k):
            popped_value = self.pop()
            top_k.append(popped_value)

        return top_k


class ParserError(Exception):
    pass


def lr_one_skeleton_parser(lexer: Lexer, states, action_table, goto_table):
    stack = Stack()

    stack.push(None)
    stack.push(("Goal", states.get_state_zero()))

    ast = AST_v2()

    word = lexer.get_next()

    while True:
        _, state = stack.get_top()

        if not isinstance(word, EOF):
            terminal = Terminal.convert_from_token(word)
        else:
            terminal = EOF()

        action = action_table.get((state, terminal))

        print(action)

        if isinstance(action, Reduce):
            action_lhs = Instance.convert_from(action.lhs)

            lhs_ast = ast.create_or_get_node(action_lhs)

            top_k = stack.pop_top_k(len(action.rhs))
            for token, _ in reversed(top_k):
                if isinstance(token, Token):
                    token = Terminal.convert_from_token(token)
                token = Instance.convert_from(token)

                i_ast = ast.create_or_get_node(token)
                lhs_ast.sub_node_list.append(i_ast)

            _, state = stack.get_top()
            goto_state = goto_table.get((state, action.lhs))

            stack.push((action_lhs, goto_state))

        elif isinstance(action, Shift):
            stack.push((word, action.next_state))

            word = lexer.get_next()

        elif isinstance(action, Accept) and word == EOF():
            ast.root_node = lhs_ast
            break

        else:
            raise ParserError()

    return ast


if __name__ == "__main__":
    class FakedLexer(List[Terminal]):
        def __init__(self, *args, **kwargs):
            self.current_offset = 0
            super().__init__(*args, **kwargs)

        def get_next(self) -> Terminal:
            if self.current_offset >= len(self):
                raise ValueError()

            token = self[self.current_offset]
            self.current_offset += 1

            return token

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

    lexer = FakedLexer([Terminal("baa", "baa"), Terminal("baa", "baa"), EOF()])

    ast = lr_one_skeleton_parser(lexer, states, action, goto_table)

    print("")
