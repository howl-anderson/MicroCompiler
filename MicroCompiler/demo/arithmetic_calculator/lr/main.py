import operator

from MicroCompiler.LR.lr_one_parser import LROneParser
from MicroCompiler.parser_evaluator import ParserEvaluator_v2
from MicroCompiler.LR.lr_one_parser_generator import LROneParserGenerator
from MicroCompiler.lexer.tokens.white_space_token import WhiteSpaceToken
from MicroCompiler.lexer.lexer import Lexer
from MicroRegEx.Token import Token
from MicroCompiler.postfix_expression.evaluator import Evaluator
from MicroCompiler.demo.arithmetic_calculator.lr.user_level_parser import Parser

user_level_parser = Parser()


def main():
    user_defined_lexer_rule = [
        # token type, token regex, token action
        ["print", r"print", lambda x: Token("print", print)],
        ["num", r"(0|1|2|3|4|5|6|7|8|9)+", lambda x: Token("num", int(x))],
        ["+", r"\+", lambda x: Token("+", operator.add)],
        ["-", r"-", lambda x: Token("-", operator.sub)],
        ["*", r"\*", lambda x: Token("*", operator.mul)],
        ["/", r"/", lambda x: Token("/", operator.truediv)],
        ["(", r"\(", lambda x: Token("(")],
        [")", r"\)", lambda x: Token(")")],
        [")", r"\)", lambda x: Token(")")],
        [";", r";", lambda x: Token(";")],
        ["white space", r" +", lambda x: WhiteSpaceToken(x)],
    ]

    lexer = Lexer(user_defined_lexer_rule)
    lexer.read_from_file("calculator_program.txt")
    lexer.parse()

    lr_one_parser_generator = LROneParserGenerator("calculator.mbnf")
    states, action_table, goto_table = lr_one_parser_generator.generate()

    lr_one_parser = LROneParser(lexer, states, action_table, goto_table)
    ast = lr_one_parser.parse()

    topological_ordered_list = ast.get_topological_ordered_list()

    parser_evaluator = ParserEvaluator_v2(user_level_parser)
    postfix_expr = parser_evaluator.eval(topological_ordered_list)

    evaluator = Evaluator(postfix_expr)
    result = evaluator.eval()

    return result


if __name__ == "__main__":
    result = main()
    print(result)
