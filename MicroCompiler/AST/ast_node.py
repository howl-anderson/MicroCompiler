from MicroCompiler.SkeletonParser import Node


class AstNode(object):
    index_counter = 0

    def __init__(self, type_, value=None, index=None):
        self.type = type_
        self.value = value
        self.index = index if index else self.index_counter

        self.increase_index_counter()

    @classmethod
    def increase_index_counter(cls):
        cls.index_counter += 1

    def access(self, visitor_object):
        func_name = visitor_object.get_method_name(self.type)
        func = getattr(visitor_object, func_name)
        return func(self)

    def __repr__(self):
        return "{}(type_={}, value={}，index={})".format(
            self.__class__.__name__, self.type, self.value, self.index
        )


class NonTerminalAstNode(AstNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sub_node_list = []

    def add_sub_node(self, node):
        self.sub_node_list.append(node)


class TerminalAstNode(AstNode):
    pass


node_registry = {}


def create_or_get_ast_node(node) -> AstNode:
    cls_name = node.__class__.__name__
    unique_index = "{}.{}".format(cls_name, node.index)
    type_, value, index = node.type, node.value, node.index if isinstance(node, Node) else None

    if unique_index not in node_registry:
        if isinstance(node, Node):
            node = NonTerminalAstNode(type_, value, index)
        else:
            node = TerminalAstNode(type_, value, index)
        node_registry[unique_index] = node

    return node_registry[unique_index]
