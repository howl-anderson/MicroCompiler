from MicroCompiler.SkeletonParser import Token, WhiteSpaceToken

lexer_define = [
    # token type, token regex, token action
    [
        "var",
        (
            r"(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)+"
            r"(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)*"
        ),
        lambda x: Token("var", str(x)),
    ],
    [
        "const",
        r"(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|,)+",
        lambda x: Token("const", str(x)),
    ],
    ["{{", "{{", lambda x: Token("{{", None)],
    ["}}", "}}", lambda x: Token("}}", None)],
    ["white space", r" +", lambda x: WhiteSpaceToken(x)],
]
