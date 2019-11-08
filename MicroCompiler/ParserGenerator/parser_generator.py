from MicroCompiler.ParserGenerator.Lexer import Lexer
from MicroCompiler.ParserGenerator.Parser import Parser


class ParserGenerator:
    def __init__(self):
        self.bnf_string = None

    def read_grammar_from_string(self, bnf_string):
        self.bnf_string = bnf_string

    def read_grammar_from_file(self, input_file):
        with open(input_file) as fd:
            self.bnf_string = fd.read()

    def generate(self):
        lexer = Lexer()
        lexer.parse(self.bnf_string)

        parser = Parser(lexer.token_list)
        parser.parse()
        productions = parser.generate_production()

        return productions
