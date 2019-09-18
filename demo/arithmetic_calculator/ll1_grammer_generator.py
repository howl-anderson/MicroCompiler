from MicroCompiler.ParserGenerator.Generator import Generator

g = Generator("calculator.mbnf")
g.generate()

g.write_yaml("calculator.yaml")
