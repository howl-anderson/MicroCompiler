from MicroCompiler.ParserGenerator.Generator import Generator

g = Generator("lox_official_grammar.mbnf")
g.generate()

g.write_yaml("lox_grammar.yaml")
