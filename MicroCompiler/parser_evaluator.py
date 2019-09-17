class ParserEvaluator(object):
    """
    Call user's parser instance (subclass of Parser), directed by topological_sorted_nodes
    """
    def __init__(self, parser_instance):
        self.parser_instance = parser_instance

    def eval(self, topological_sorted_nodes):
        for cmd in topological_sorted_nodes:
            cmd_prototype = cmd["prototype"]
            cmd_reference = cmd["reference"]
            if cmd_prototype.__class__.__name__ == "Token":
                # token value already set
                continue

            if cmd_prototype.__class__.__name__ == "Node":
                values = [i.reference.value for i in cmd_reference.sub_node_list]
                method_name = cmd_prototype.type
                legal_method_name = self.parser_instance.get_legal_method_name(method_name)
                method_func = getattr(
                    self.parser_instance, legal_method_name, self.parser_instance.fallback
                )
                return_value = method_func(values)
                cmd["reference"].reference.value = return_value

        final_value = cmd["reference"].reference.value

        return final_value
