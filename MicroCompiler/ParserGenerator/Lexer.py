from MicroCompiler.ParserGenerator.Lexeme import Lexeme
from MicroCompiler.ParserGenerator.Lexeme import (
    NON_TERMINAL,
    TERMINAL,
    PRODUCT,
    ALTERNATIVE,
    SEMICOLON,
    EPSILON,
)


class Lexer:
    def __init__(self):
        self.token_list = []

    def parse(self, string_: str):
        raw_token_list = string_.split()
        for raw_token in raw_token_list:
            if raw_token.isalpha():
                if raw_token == "ϵ":
                    symbol = Lexeme(EPSILON, raw_token)
                    self.token_list.append(symbol)
                else:
                    non_terminal = Lexeme(NON_TERMINAL, raw_token)
                    self.token_list.append(non_terminal)
            elif raw_token == "|":
                terminal = Lexeme(ALTERNATIVE, raw_token)
                self.token_list.append(terminal)
            elif raw_token == "->":
                terminal = Lexeme(PRODUCT, raw_token)
                self.token_list.append(terminal)
            elif raw_token == ";":
                terminal = Lexeme(SEMICOLON, raw_token)
                self.token_list.append(terminal)
            elif raw_token.startswith("'"):
                terminal = Lexeme(TERMINAL, raw_token[1:-1])
                self.token_list.append(terminal)

            else:
                raise ValueError("{} is not a valid token".format(raw_token))
