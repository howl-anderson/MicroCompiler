from MicroCompiler.ParserGenerator.Generator import Generator
from MicroCompiler.SkeletonParser import Token
from demo.template_engine.render_engine import render_engine
from demo.template_engine.user_level_parser import Parser


def render_with_tokens(token_list, data):
    # BNF to LL1
    g = Generator("syntax.mbnf")
    g.generate()
    g.write_yaml("syntax.yaml")

    # Node walker
    user_level_parser = Parser(data)

    return render_engine(
        "syntax.yaml", token_list, user_level_parser, "syntax.graphml"
    )


if __name__ == "__main__":
    # equal to: `Hello, {{ name }}`
    token_list = [
        Token("const", "Hello, "),
        Token("{{", None),
        Token("var", "name"),
        Token("}}", None),
        Token("<EOF>"),
    ]

    result = render_with_tokens(token_list, {"name": "Xiaoquan"})
    print(result)
