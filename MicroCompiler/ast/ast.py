from typing import Union, Tuple, List

import networkx as nx

from MicroCompiler.ast import TerminalInstance, NonTerminalInstance
from MicroCompiler.ast.ast_node import NonTerminalAstNode_v2, \
    TerminalAstNode_v2


class AST(object):
    def __init__(self, root_node):
        self.root_node = root_node


class AST_v2(object):
    def __init__(self):
        self.node_registry = {}

        self.root_node = None

    def set_root_node(self, node: NonTerminalAstNode_v2):
        self.root_node = node

    @staticmethod
    def _get_node_unique_id(node):
        return "{}.{}".format(node.__class__.__name__, node.index)

    def create_or_get_node(self, node: Union[TerminalInstance, NonTerminalInstance]) -> Union[NonTerminalAstNode_v2, TerminalAstNode_v2]:
        node_unique_id = self._get_node_unique_id(node)

        if node_unique_id not in self.node_registry:
            node_name = node.value

            if isinstance(node, NonTerminalInstance):
                ast_node = NonTerminalAstNode_v2(node_name)
            else:
                ast_node = TerminalAstNode_v2(node_name)

            ast_node.data = node
            self.node_registry[node_unique_id] = ast_node

        return self.node_registry[node_unique_id]

    def walk(self) -> Tuple[NonTerminalAstNode_v2, Union[Union[NonTerminalAstNode_v2, TerminalAstNode_v2]]]:
        return self.walk_from_node(self.root_node)

    def walk_from_node(self, node: Union[NonTerminalAstNode_v2, TerminalAstNode_v2]):
        # TODO: change to work list otherwise will get maximum recursion depth in long program
        if isinstance(node, TerminalAstNode_v2):
            return []

        for sub_node in node.sub_node_list:
            yield node, sub_node

            for i in self.walk_from_node(sub_node):
                yield i

    def generate_graph(self) -> nx.DiGraph:
        graph = nx.DiGraph()

        for parent_node, child_node in self.walk():
            parent_node_label = str(parent_node)
            child_node_label = str(child_node)

            graph.add_node(parent_node_label, data=parent_node)
            graph.add_node(child_node_label, data=child_node)

            # order: parent node to child node
            graph.add_edge(child_node_label, parent_node_label)

        return graph

    def write_to_graphml(self, graphml_file):
        graph = self.generate_graph()

        # remove data attribute which is not writeable for graphml
        for node_id in nx.classes.function.nodes(graph):
            node = graph.nodes[node_id]
            del node["data"]

        nx.write_graphml(graph, graphml_file)

    def get_topological_ordered_list(self) -> List[Union[NonTerminalAstNode_v2, TerminalAstNode_v2]]:
        graph = self.generate_graph()

        return [graph.nodes[node_id]["data"] for node_id in nx.topological_sort(graph)]
