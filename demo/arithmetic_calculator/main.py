import operator

from MicroCompiler.ParserGenerator.Generator import Generator
from MicroCompiler.SkeletonParser import Token
from demo.arithmetic_calculator.arithmetic_calculator import arithmetic_calculator
from demo.arithmetic_calculator.user_level_parser import Parser

user_level_parser = Parser()


def main(token_list):
    g = Generator("calculator.mbnf")
    g.generate()
    g.write_yaml("calculator.yaml")

    result = arithmetic_calculator("calculator.yaml", token_list, user_level_parser, "calculator.graphml")
    print(result)


if __name__ == "__main__":
    # equal to: 6 * (2 + 2）
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

    main(token_list)
