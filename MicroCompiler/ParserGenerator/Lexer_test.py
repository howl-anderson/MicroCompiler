import unittest

from .Lexer import Lexer
from .Lexeme import Lexeme
from .Lexeme import  (
    NON_TERMINAL,
    TERMINAL,
    PRODUCT,
    SEMICOLON,
    ALTERNATIVE
)


class TestLexer(unittest.TestCase):
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
        real_result = lexer.token_list

        expect_result = [Lexeme(NON_TERMINAL, 'statement'),
                         Lexeme(PRODUCT, '->'),
                         Lexeme(NON_TERMINAL, 'expression'),
                         Lexeme(TERMINAL, ';'),
                         Lexeme(SEMICOLON, ';'),
                         Lexeme(NON_TERMINAL, 'expression'),
                         Lexeme(PRODUCT, '->'),
                         Lexeme(TERMINAL, 'plus'),
                         Lexeme(ALTERNATIVE, '|'),
                         Lexeme(TERMINAL, 'minus'),
                         Lexeme(SEMICOLON, ';')]

        self.assertEqual(real_result, expect_result)