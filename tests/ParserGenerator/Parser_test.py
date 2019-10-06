import unittest

from MicroCompiler.ParserGenerator.Lexer import Lexer
from MicroCompiler.ParserGenerator.Parser import Parser
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.Lookahead.Terminal import CHARACTER


class TestParser(unittest.TestCase):
    def test_simple_case(self):
        mbnf = """
        statement ->
            expression ';'
            ;

        expression ->
            'plus'
            | 'minus'
            ;
        """

        lexer = Lexer()
        lexer.parse(mbnf)

        parser = Parser(lexer.token_list)
        parser.parse()
        real_result = parser.generate_production()

        except_result = {
            NonTerminal("expression"): [
                [Terminal(CHARACTER, "plus")],
                [Terminal(CHARACTER, "minus")],
            ],
            NonTerminal("statement"): [
                [NonTerminal("expression"), Terminal(CHARACTER, ";")]
            ],
        }

        self.assertEqual(dict(real_result), except_result)
        self.assertEqual(real_result.start_symbol, NonTerminal("statement"))
