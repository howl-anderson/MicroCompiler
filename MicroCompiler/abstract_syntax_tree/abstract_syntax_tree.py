class AbstractSyntaxTree(object):
    def __init__(self):
        self.start_node = None

    def set_start_node(self, node):
        self.start_node = node

    def add_production(self, from_node, to_node):
        from_node.add_sub_node(to_node)
