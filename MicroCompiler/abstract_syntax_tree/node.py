class Node(object):
    def __init__(self, label_str=None, reference=None):
        self.label_str = label_str
        self.reference = reference
        self.sub_node_list = []

    def add_sub_node(self, node):
        self.sub_node_list.append(node)

    def __repr__(self):
        return "{}(label_str={}, reference={}, sub_node_list={})".format(
            self.__class__.__name__, self.label_str, self.reference, self.sub_node_list
        )


node_registry = {}


def create_or_get_node(node):
    cls_name = node.__class__.__name__

    node_id = "{}.{}".format(cls_name, node.index)
    label_str = "{}.{}.{}".format(node.type, cls_name, node.index)
    reference = node

    if node_id in node_registry:
        return node_registry[node_id]

    node = Node(label_str, reference)
    node_registry[node_id] = node

    return node
