import operator

from MicroCompiler.SkeletonParser import Token
from demo.arithmetic_calculator.arithmetic_calculator import arithmetic_calculator
from demo.arithmetic_calculator.user_level_parser import Parser

user_level_parser = Parser()
# token_list = [
#     Token("num", 6),
#     Token("/", operator.truediv),
#     Token("num", 2),
#     Token("<EOF>"),
# ]
token_list = [
    Token("num", 6),
    Token("*", operator.mul),
    Token("("),
    Token("num", 2),
    Token("+", operator.add),
    Token("num", 2),
    Token(")"),
    Token("<EOF>"),
]

result = arithmetic_calculator("output.yaml", token_list, user_level_parser)
print(result)
