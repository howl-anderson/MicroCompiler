import operator
import os

from MicroCompiler.LR.lr_one_parser import LROneParser
from MicroCompiler.parser_evaluator import ParserEvaluator_v2
from MicroCompiler.LR.lr_one_parser_generator import LROneParserGenerator
from MicroCompiler.lexer.tokens import WhiteSpaceToken
from MicroCompiler.lexer.lexer import Lexer
from MicroCompiler.lexer.tokens.token import Token
from MicroCompiler.postfix_expression.evaluator import Evaluator
from MicroCompiler.demo.sheep_noise.user_level_parser import Parser

user_level_parser = Parser()

user_defined_lexer_rule = [
    # token type, token regex, token action
    ["baa", r"baa", lambda x: Token("baa", None)],
    ["white space", r" +", lambda x: WhiteSpaceToken(x)],
]

current_dir = os.path.dirname(os.path.realpath(__file__))

GRAMMAR_DEFINE_FILE = os.path.join(current_dir, "sheep_noise.mbnf")


class SheepNoise:
    def __init__(self):
        self.lexer = self._init_lexer()

        self.states, self.action_table, self.goto_table = self._init_lr_knowledge()

    @staticmethod
    def _init_lexer():
        lexer = Lexer(user_defined_lexer_rule)
        return lexer

    @staticmethod
    def _init_lr_knowledge():
        lr_one_parser_generator = LROneParserGenerator(GRAMMAR_DEFINE_FILE)
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
        result = parser_evaluator.eval(topological_ordered_list)

        return result


if __name__ == "__main__":
    ac = SheepNoise()
    result = ac.eval("baa   baa baa  baa")
    print(result)
