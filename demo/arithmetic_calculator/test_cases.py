from MicroCompiler.SkeletonParser import Token
import operator

test_cases = (
    (
        [
            Token("num", 6),
            Token("+", operator.add),
            Token("num", 2),
            Token("<EOF>"),
        ],
        8,
    ),
    (
        [
            Token("num", 6),
            Token("+", operator.add),
            Token("num", 2),
            Token("+", operator.add),
            Token("num", 2),
            Token("<EOF>"),
        ],
        10,
    ),
    (
        [
            Token("num", 6),
            Token("-", operator.sub),
            Token("num", 2),
            Token("<EOF>"),
        ],
        4,
    ),
    (
        [
            Token("num", 6),
            Token("-", operator.sub),
            Token("num", 2),
            Token("-", operator.sub),
            Token("num", 2),
            Token("<EOF>"),
        ],
        2,
    ),
    (
        [
            Token("num", 6),
            Token("/", operator.truediv),
            Token("num", 2),
            Token("<EOF>"),
        ],
        3.0,
    ),
    (
        [
            Token("num", 12),
            Token("/", operator.truediv),
            Token("num", 6),
            Token("/", operator.truediv),
            Token("num", 2),
            Token("<EOF>"),
        ],
        1,
    ),
    (
        [
            Token("num", 6),
            Token("*", operator.mul),
            Token("num", 2),
            Token("<EOF>"),
        ],
        12,
    ),
    (
        [
            Token("num", 3),
            Token("*", operator.mul),
            Token("num", 6),
            Token("*", operator.mul),
            Token("num", 2),
            Token("<EOF>"),
        ],
        36,
    ),
    (
        [
            Token("num", 6),
            Token("+", operator.add),
            Token("num", 2),
            Token("/", operator.truediv),
            Token("num", 2),
            Token("<EOF>"),
        ],
        7,
    ),
    (
        [
            Token("num", 6),
            Token("/", operator.truediv),
            Token("num", 2),
            Token("+", operator.add),
            Token("num", 2),
            Token("<EOF>"),
        ],
        5,
    ),
    (
        [
            Token("num", 6),
            Token("+", operator.add),
            Token("num", 2),
            Token("*", operator.mul),
            Token("num", 2),
            Token("<EOF>"),
        ],
        10,
    ),
    (
        [
            Token("num", 6),
            Token("*", operator.mul),
            Token("num", 2),
            Token("+", operator.add),
            Token("num", 2),
            Token("<EOF>"),
        ],
        14,
    ),
    (
        [
            Token("num", 6),
            Token("*", operator.mul),
            Token("("),
            Token("num", 2),
            Token("+", operator.add),
            Token("num", 2),
            Token(")"),
            Token("<EOF>"),
        ],
        24,
    ),
    (
        [
            Token("("),
            Token("num", 2),
            Token("+", operator.add),
            Token("num", 2),
            Token(")"),
            Token("*", operator.mul),
            Token("num", 6),
            Token("<EOF>"),
        ],
        24,
    ),
    (
        [
            Token("("),
            Token("num", 2),
            Token("+", operator.add),
            Token("num", 2),
            Token("+", operator.add),
            Token("num", 2),
            Token(")"),
            Token("*", operator.mul),
            Token("num", 6),
            Token("<EOF>"),
        ],
        36,
    ),
    (
        [
            Token("("),
            Token("num", 2),
            Token("+", operator.add),
            Token("num", 2),
            Token("/", operator.truediv),
            Token("num", 2),
            Token(")"),
            Token("*", operator.mul),
            Token("num", 6),
            Token("<EOF>"),
        ],
        18,
    ),
)
