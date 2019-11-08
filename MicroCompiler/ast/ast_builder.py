from MicroCompiler.ast.ast_node import create_or_get_ast_node
from MicroCompiler.ast.ast import AST


def build_ast_from_call_stack(call_stack):
    root = call_stack[0][0]
    root_node = create_or_get_ast_node(root)
    ast = AST(root_node)

    for start, end in call_stack:
        start_node = create_or_get_ast_node(start)
        end_node = create_or_get_ast_node(end)
        start_node.add_sub_node(end_node)

    return ast
