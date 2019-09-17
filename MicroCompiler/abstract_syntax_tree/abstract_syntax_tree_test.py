import operator

from MicroCompiler.SkeletonParser import Token, SkeletonParser, Epsilon
from MicroCompiler.parser_builder import ParserBuilder
from MicroCompiler.postfix_expression.operator import PythonBuiltinOperator

token_list = [Token("num", 6), Token("/", operator.truediv), Token("num", 2), Token("<EOF>")]
# token_list = [
#     Token("num", 6),
#     Token("/", operator.truediv),
#     Token("num", 2),
#     Token("/", operator.truediv),
#     Token("num", 2),
#     Token("<EOF>"),
# ]


sp = SkeletonParser("output.yaml", token_list)
sp.parse()

from MicroCompiler.abstract_syntax_tree.abstract_syntax_tree import (
    AbstractSyntaxTree as AST,
)
from MicroCompiler.abstract_syntax_tree.node import create_or_get_node

import matplotlib.pyplot as plt

import networkx as nx

DG = nx.DiGraph()

ast = AST()


def fallback_method(*args, **kwargs):
    print(*args, **kwargs)
    return "Done!"


def get_node_label(obj):
    if obj.value is not None:
        return "{}.{}.{}#{}".format(
            obj.__class__.__name__, obj.type, obj.value, obj.index
        )

    return "{}.{}#{}".format(obj.__class__.__name__, obj.type, obj.index)


for parser_instance, (f, t) in enumerate(sp.call_stack):
    from_node = create_or_get_node(f)
    to_node = create_or_get_node(t)
    if parser_instance == 0:
        ast.set_start_node(from_node)

    ast.add_production(from_node, to_node)

    f_label = get_node_label(f)
    t_label = get_node_label(t)

    DG.add_node(f_label, prototype=f, reference=from_node)
    DG.add_node(t_label, prototype=t, reference=to_node)

    DG.add_edge(t_label, f_label)  # sub node to node

print("")

# nx.draw(DG)

# plt.show()

# nx.write_graphml(DG, "data.graphml")
# nx.write_gexf(DG, "data.gexf")

ordered_list = list(nx.topological_sort(DG))

pb = ParserBuilder()
pb.add_generator("failback", "Who Am I")
clazz = pb.generate()


class Parser(clazz):
    def __init__(self):
        self.post_expr = []

    def ExprTwo(self, input_):
        # ExprTwo -> '+' Term ExprTwo
        #          | '-' Term ExprTwo
        #          | ϵ ;

        if len(input_) == 1:
            # ExprTwo -> ϵ
            return Epsilon()

        if isinstance(input_[2], Epsilon):
            # ExprTwo -> '+' Term ExprTwo | '-' Term ExprTwo
            #                        |                  |
            #                        -> ϵ               -> ϵ
            return input_[:2]

        if isinstance(input_[2], list):
            # ExprTwo -> '+' Term ExprTwo | '-' Term ExprTwo
            #                        |                  |
            #                        -> ['+' num]       -> ['-' num]
            post_expr = []

            # value #1
            if isinstance(input_[1], list):
                post_expr.extend(input_[1])
            else:
                post_expr.append(input_[1])

            # value #2
            if isinstance(input_[2][1], list):
                post_expr.extend(input_[2][1])
            else:
                post_expr.append(input_[2][1])

            post_expr.append(input_[2][0])  # op

            return [input_[0], post_expr]

    def TermTwo(self, input_):
        # TermTwo -> '*' Factor TermTwo
        #          | '/' Factor TermTwo
        #          | ϵ ;

        if len(input_) == 1:
            # ExprTwo -> ϵ
            return Epsilon()

        if isinstance(input_[2], Epsilon):
            # ExprTwo -> '+' Term ExprTwo | '-' Term ExprTwo
            #                        |                  |
            #                        -> ϵ               -> ϵ
            return input_[:2]

        if isinstance(input_[2], list):
            # TermTwo -> '*' Factor TermTwo | '/' Factor TermTwo
            #                         |                    |
            #                         -> ['/' num]          -> ['*' num]
            post_expr = []

            # value #1
            if isinstance(input_[1], list):
                post_expr.extend(input_[1])
            else:
                post_expr.append(input_[1])

            # value #2
            if isinstance(input_[2][1], list):
                post_expr.extend(input_[2][1])
            else:
                post_expr.append(input_[2][1])

            post_expr.append(input_[2][0])  # op

            return [input_[0], post_expr]

    def num(self, input_):
        return input_[0]

    def Factor(self, input_):
        if len(input_) == 1:
            return input_[0]

        if len(input_) == 3:
            print(input_)
            return input_[1]

    def Division(self, input_):
        return PythonBuiltinOperator(input_[0], 2)

    def Term(self, input_):
        if isinstance(input_[1], Epsilon):
            return input_[0]

        post_expr = []

        # value #1
        if isinstance(input_[0], list):
            post_expr.extend(input_[0])
        else:
            post_expr.append(input_[0])

        # value #2
        if isinstance(input_[1][1], list):
            post_expr.extend(input_[1][1])
        else:
            post_expr.append(input_[1][1])

        post_expr.append(input_[1][0])  # op

        return post_expr

    def Expr(self, input_):
        if isinstance(input_[1], Epsilon):
            return input_[0]

    def Goal(self, input_):
        return input_[0]

    def Start(self, input_):
        return input_[0]


parser_instance = Parser()

topological_ordered_list = [DG.nodes[i] for i in nx.topological_sort(DG)]

from MicroCompiler.parser_evaluator import ParserEvaluator

parser_evaluator = ParserEvaluator(parser_instance)
final_value = parser_evaluator.eval(topological_ordered_list)

print("")

from MicroCompiler.postfix_expression.evaluator import Evaluator

evaluator = Evaluator(final_value)
result = evaluator.eval()

print("")
