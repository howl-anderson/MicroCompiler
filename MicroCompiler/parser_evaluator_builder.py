import networkx as nx

from MicroCompiler.abstract_syntax_tree.abstract_syntax_tree import (
    AbstractSyntaxTree as AST,
)
from MicroCompiler.abstract_syntax_tree.node import create_or_get_node


def build_parser_evaluator(call_stack, graph_file=None):
    DG = nx.DiGraph()

    graph = nx.DiGraph()

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

    for parser_instance, (f, t) in enumerate(call_stack):
        from_node = create_or_get_node(f)
        to_node = create_or_get_node(t)
        if parser_instance == 0:
            ast.set_start_node(from_node)

        ast.add_production(from_node, to_node)

        f_label = get_node_label(f)
        t_label = get_node_label(t)

        DG.add_node(f_label, prototype=f, reference=from_node)
        DG.add_node(t_label, prototype=t, reference=to_node)

        graph.add_node(f_label)
        graph.add_node(t_label)

        DG.add_edge(t_label, f_label)  # sub node to node
        graph.add_edge(t_label, f_label)  # sub node to node

    topological_ordered_list = [DG.nodes[i] for i in nx.topological_sort(DG)]

    if graph_file:
        nx.write_graphml(graph, graph_file)

    return topological_ordered_list
