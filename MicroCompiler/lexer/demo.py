from MicroCompiler.lexer.lexer import lex_analysis

from MicroCompiler.lexer.tokens import Token, WhiteSpaceToken

lexer_define = [
    # token type, token regex, token action
    ["num", r"(0|1|2|3|4|5|6|7|8|9)+", lambda x: Token("num", int(x))],
    ["+", r"\+", lambda x: Token("+")],
    ["-", r"-", lambda x: Token("-")],
    ["*", r"\*", lambda x: Token("*")],
    ["/", r"/", lambda x: Token("/")],
    ["(", r"\(", lambda x: Token("(")],
    [")", r"\)", lambda x: Token(")")],
    ["white space", r" +", lambda x: WhiteSpaceToken(x)],
]


input_string = "2+3 *  6"
result = lex_analysis(input_string, lexer_define)

print(result)
