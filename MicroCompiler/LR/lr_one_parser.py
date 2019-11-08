import operator
import pickle

from MicroCompiler.LR.lr_one_skeleton_parser import lr_one_skeleton_parser
from MicroCompiler.SkeletonParser import WhiteSpaceToken
from MicroCompiler.lexer.lexer import Lexer
from MicroCompiler.lexer.tokens import Token


class LROneParser(object):
    def __init__(self, lexer, states, action_table, goto_table):
        self.lexer = lexer
        self.states = states
        self.action_table = action_table
        self.goto_table = goto_table

    def parse(self):
        return lr_one_skeleton_parser(
            self.lexer, self.states, self.action_table, self.goto_table
        )


if __name__ == "__main__":
    lexer = Lexer(
        [
            # token type, token regex, token action
            ["print", r"print", lambda x: Token("print", print)],
            ["num", r"(0|1|2|3|4|5|6|7|8|9)+", lambda x: Token("num", int(x))],
            ["+", r"\+", lambda x: Token("+", operator.add)],
            ["-", r"-", lambda x: Token("-", operator.sub)],
            ["*", r"\*", lambda x: Token("*", operator.mul)],
            ["/", r"/", lambda x: Token("/", operator.truediv)],
            ["(", r"\(", lambda x: Token("(")],
            [")", r"\)", lambda x: Token(")")],
            [")", r"\)", lambda x: Token(")")],
            [";", r";", lambda x: Token(";")],
            ["white space", r" +", lambda x: WhiteSpaceToken(x)],
        ]
    )
    lexer.read_from_file("calculator_program.txt")
    lexer.parse()

    with open("knowledge.pkl", 'rb') as fd:
        states, action_table, goto_table = pickle.load(fd)

    lr_one_parser = LROneParser(lexer, states, action_table, goto_table)
    ast = lr_one_parser.parse()

    ast.write_to_graphml("test.graphml")

    print("")
