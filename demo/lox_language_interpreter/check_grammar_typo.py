from MicroCompiler.ParserGenerator import ParserGenerator

pg = ParserGenerator()
pg.read_grammar_from_file("lox_official_grammar.mbnf")
productions = pg.generate()
productions.write_to_file("generated_grammar.mbnf")

