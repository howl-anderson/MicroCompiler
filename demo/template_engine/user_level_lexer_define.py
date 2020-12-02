import operator

from MicroCompiler.SkeletonParser import Token, WhiteSpaceToken

lexer_define = [
    # token type, token regex, token action
    ["num", r"(0|1|2|3|4|5|6|7|8|9)+", lambda x: Token("num", int(x))],
    ["+", r"\+", lambda x: Token("+", operator.add)],
    ["-", r"-", lambda x: Token("-", operator.sub)],
    ["*", r"\*", lambda x: Token("*", operator.mul)],
    ["/", r"/", lambda x: Token("/", operator.truediv)],
    ["(", r"\(", lambda x: Token("(")],
    [")", r"\)", lambda x: Token(")")],
    ["white space", r" +", lambda x: WhiteSpaceToken(x)],
]