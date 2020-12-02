from MicroCompiler.SkeletonParser import SkeletonParser
from MicroCompiler.parser_evaluator import ParserEvaluator
from MicroCompiler.parser_evaluator_builder import build_parser_evaluator


def render_engine(grammar_file, token_list, user_level_parser, graph_file=None):
    sp = SkeletonParser(grammar_file, token_list)
    sp.parse()

    topological_ordered_list = build_parser_evaluator(sp.call_stack, graph_file)

    parser_evaluator = ParserEvaluator(user_level_parser)
    result = parser_evaluator.eval(topological_ordered_list)

    return result
