from MicroCompiler.lexer.user_level_lexer_define import lexer_define

from MicroCompiler.lexer.lexer import lex_analysis

input_string = "2+3 *  6"
result = lex_analysis(input_string, lexer_define)

print("")
