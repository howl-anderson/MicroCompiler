from MicroCompiler.ast.ast import AST_v2
from MicroCompiler.cfg import NonTerminal
from MicroCompiler.cfg import Terminal


class Stack(list):
    pass


def test_bottom_up_parser():
    ast = AST_v2()

    num_0 = Terminal("num")
    factor_1 = NonTerminal("Factor")
    term_2 = NonTerminal("Term")
    expr_3 = NonTerminal("Expr")
    num_4 = Terminal("num")
    factor_5 = NonTerminal("Factor")
    term_6 = NonTerminal("Term")
    plus_7 = Terminal("+")
    expr_8 = NonTerminal("Expr")

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
