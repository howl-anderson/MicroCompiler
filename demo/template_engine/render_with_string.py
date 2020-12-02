from MicroCompiler.SkeletonParser import Token, WhiteSpaceToken
from MicroCompiler.lexer.lexer import lex_analysis
from demo.template_engine.render_with_tokens import render_with_tokens
from demo.template_engine.user_level_lexer_define import lexer_define


def render_with_string(input_string, data):
    raw_token_list = [i[1] for i in lex_analysis(input_string, lexer_define)]
    # remote whitespace token
    token_list = list(
        filter(lambda x: not isinstance(x, WhiteSpaceToken), raw_token_list)
    )
    # append EOF token
    token_list.append(Token("<EOF>"))

    return render_with_tokens(token_list, data)


if __name__ == "__main__":
    input_string = "HELLO,{{ name }}"

    result = render_with_string(input_string, {"name": "Xiaoquan"})

    print(result)
