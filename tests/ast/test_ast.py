from typing import Union

from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.ast.ast import AST_v2


NT = NonTerminal


T = Terminal


class Stack(list):
    pass


def test_bottom_up_parser():
    ast = AST_v2()

    num_0 = T(None, "num")
    factor_1 = NT("Factor")
    term_2 = NT("Term")
    expr_3 = NT("Expr")
    num_4 = T(None, "num")
    factor_5 = NT("Factor")
    term_6 = NT("Term")
    plus_7 = T(None, "+")
    expr_8 = NT("Expr")

    parser_build_action = [
        (factor_1, (num_0,)),
        (term_2, (factor_1,)),
        (expr_3, (term_2,)),
        (factor_5, (num_4,)),
        (term_6, (factor_5,)),
        (expr_8, (expr_3, plus_7, term_6)),
    ]

    for lhs, rhs in parser_build_action:
        lhs_ast = ast.create_or_get_node(lhs)

        for i in rhs:
            i_ast = ast.create_or_get_node(i)

            lhs_ast.add_sub_node(i_ast)

        print("")

    # setup root node
    ast.set_root_node(ast.create_or_get_node(lhs))

    print("")

    for i in ast.walk():
        print(i)

    print("")

    ast.write_to_graphml("test.graphml")

    top_ordered_list = ast.get_topological_ordered_list()

    print("")
