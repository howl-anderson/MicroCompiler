from MicroCompiler.cfg import NonTerminal
from MicroCompiler.cfg import Terminal
from MicroCompiler.ParserGenerator.Generator import Generator


def test_construct_simple(datadir):
    g = Generator(datadir / "sample.mbnf")
    real_result = g.generate()

    expect_result = {
        NonTerminal("statement"): {
            Terminal("plus"): 0,
            Terminal(";"): "--",
            Terminal("minus"): 0,
        },
        NonTerminal("expression"): {
            Terminal("plus"): 1,
            Terminal(";"): "--",
            Terminal("minus"): 2,
        },
    }

    assert real_result == expect_result

    g.write_yaml("../output.yaml")
