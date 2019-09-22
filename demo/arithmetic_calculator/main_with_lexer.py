import os

from MicroCompiler.ParserGenerator.Generator import Generator
from MicroCompiler.SkeletonParser import Token, WhiteSpaceToken
from demo.arithmetic_calculator.arithmetic_calculator import arithmetic_calculator
from demo.arithmetic_calculator.user_level_parser import Parser

user_level_parser = Parser()

from MicroCompiler.lexer.user_level_lexer_define import lexer_define

from MicroCompiler.lexer.lexer import lex_analysis

current_dir = os.path.dirname(os.path.realpath(__file__))

bnf_file = os.path.join(current_dir, "calculator.mbnf")
ll1_grammar_file = os.path.join(current_dir, "calculator.yaml")
graph_file = os.path.join(current_dir, "calculator.graphml")


def main(input_string):
    raw_token_list = [i[1] for i in lex_analysis(input_string, lexer_define)]
    # remote whitespace token
    token_list = list(filter(lambda x: not isinstance(x, WhiteSpaceToken), raw_token_list))
    # append EOF token
    token_list.append(Token("<EOF>"))

    g = Generator(bnf_file)
    g.generate()
    g.write_yaml(ll1_grammar_file)

    result = arithmetic_calculator(ll1_grammar_file, token_list, user_level_parser, graph_file)
    print(result)


if __name__ == "__main__":
    input_string = "2+3 *  6"

    main(input_string)