from demo.lox_language.lox_interpreter import lox_interpreter
from demo.arithmetic_calculator.user_level_parser import Parser
from MicroCompiler.SkeletonParser import Token

user_level_parser = Parser()

token_list = [
    Token('var'), Token('id', 'x'), Token('='), Token('num', 3), Token(';'),
    Token('print'), Token('id', 'x'), Token(';'),
    Token('fun'), Token('id', 'func'), Token('('), Token('id', 'i'), Token(')'), Token('{'),
        Token('print'), Token('id', 'i'), Token(';'),
    Token('}'),
    Token('id', 'func'), Token('('), Token('num', 9), Token(')'), Token(';'),
    Token("<EOF>"),
]

# token_list = [Token("num", 6), Token("+"), Token("num", 2), Token("<EOF>")]
print("working on: ", token_list)
result = lox_interpreter(
    "lox_grammar.yaml", token_list, user_level_parser, "ast.graphml"
)
