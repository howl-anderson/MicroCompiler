from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import CHARACTER
from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.ParserGenerator.Generator import Generator


def test_construct_simple(datadir):
    g = Generator(datadir / "sample.mbnf")
    real_result = g.generate()

    expect_result = {
        NonTerminal("statement"): {
            Terminal(CHARACTER, "plus"): 0,
            Terminal(CHARACTER, ";"): "--",
            Terminal(CHARACTER, "minus"): 0,
        },
        NonTerminal("expression"): {
            Terminal(CHARACTER, "plus"): 1,
            Terminal(CHARACTER, ";"): "--",
            Terminal(CHARACTER, "minus"): 2,
        },
    }

    g.write_yaml("../output.yaml")
