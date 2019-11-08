import operator

from MicroCompiler.LR.lr_one_parser import LROneParser
from MicroCompiler.parser_evaluator import ParserEvaluator_v2
from MicroCompiler.LR.lr_one_parser_generator import LROneParserGenerator
from MicroCompiler.SkeletonParser import WhiteSpaceToken
from MicroCompiler.lexer.lexer import Lexer
from MicroCompiler.lexer.tokens.token import Token
from MicroCompiler.postfix_expression.evaluator import Evaluator
from demo.arithmetic_calculator_power_by_lr.user_level_parser import Parser

user_level_parser = Parser()

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


class ArithmeticCalculator:
    def __init__(self):
        self.lexer = self._init_lexer()

        self.states, self.action_table, self.goto_table = self._init_lr_knowledge()

    @staticmethod
    def _init_lexer():
        lexer = Lexer(user_defined_lexer_rule)
        return lexer

    @staticmethod
    def _init_lr_knowledge():
        lr_one_parser_generator = LROneParserGenerator("calculator.mbnf")
        states, action_table, goto_table = lr_one_parser_generator.generate()

        return states, action_table, goto_table

    def eval(self, user_input_string):
        self.lexer.read_from_string(user_input_string)
        self.lexer.reset()
        self.lexer.parse()

        lr_one_parser = LROneParser(self.lexer, self.states, self.action_table,
                                    self.goto_table)
        ast = lr_one_parser.parse()

        topological_ordered_list = ast.get_topological_ordered_list()

        parser_evaluator = ParserEvaluator_v2(user_level_parser)
        postfix_expr = parser_evaluator.eval(topological_ordered_list)

        evaluator = Evaluator(postfix_expr)
        result = evaluator.eval()

        return result


if __name__ == "__main__":
    ac = ArithmeticCalculator()
    result = ac.eval("6+2+2")
    print(result)
