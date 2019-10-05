from MicroCompiler.SkeletonParser import SkeletonParser
from demo.lox_language.visitor import Interpreter
from MicroCompiler.AST.ast_builder import build_ast_from_call_stack


def lox_interpreter(grammar_file, token_list, user_level_parser, graph_file=None):
    sp = SkeletonParser(grammar_file, token_list)
    sp.parse()

    ast = build_ast_from_call_stack(sp.call_stack)

    interpreter = Interpreter()

    ast.root_node.access(interpreter)
