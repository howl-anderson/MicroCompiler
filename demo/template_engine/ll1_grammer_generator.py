from MicroCompiler.ParserGenerator.Generator import Generator

g = Generator("syntax.mbnf")
g.generate()

g.write_yaml("syntax.yaml")
