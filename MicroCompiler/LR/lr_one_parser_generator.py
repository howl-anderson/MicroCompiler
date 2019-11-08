from MicroCompiler.LR.canonical_collectoin_builder import \
    canonical_collection_builder
from MicroCompiler.LR.lr_one_item import LR1Item
from MicroCompiler.LR.rhs import RightHandSide
from MicroCompiler.LR.table_construction_builder import \
    table_construction_builder
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.FirstSet import FirstSet
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.ParserGenerator import ParserGenerator
from MicroCompiler.ParserGenerator.Lexer import Lexer
from MicroCompiler.ParserGenerator.Parser import Parser


class LROneParserGenerator(object):
    def __init__(self, grammar_file: str):
        self.grammar_file = grammar_file

    def construct_lr_one_item_from_production(self, lhs, rhs, mark_at_end=False):
        mark_offset = len(rhs) if mark_at_end else 0
        lr_one_item = LR1Item(
            lhs, RightHandSide(rhs, mark_offset),
            EOF()
        )
        return lr_one_item

    def generate(self):
        pg = ParserGenerator()
        pg.read_grammar_from_file(self.grammar_file)
        productions = pg.generate()

        # end_point = LR1Item(
        #     NonTerminal("Goal"), RightHandSide([NonTerminal("SheepNoise")], 1),
        #     EOF()
        # )
        end_point = self.construct_lr_one_item_from_production(
            productions.start_symbol,
            productions[productions.start_symbol][0],
            mark_at_end=True
        )

        # start_point = {
        #     LR1Item(
        #         NonTerminal("Goal"),
        #         RightHandSide([NonTerminal("SheepNoise")], 0), EOF()
        #     )
        # }
        start_point = {
            self.construct_lr_one_item_from_production(
                productions.start_symbol,
                productions[productions.start_symbol][0],
                mark_at_end=False
            )
        }

        first_set = FirstSet(productions)
        first_set.compute()

        states = canonical_collection_builder(start_point, productions,
                                              first_set)

        action_table, goto_table = table_construction_builder(
            states, productions, first_set, end_point
        )

        return states, action_table, goto_table


if __name__ == "__main__":
    lr_one_parser_generator = LROneParserGenerator("/Users/howl/PyCharmProjects/MicroCompiler/demo/arithmetic_calculator_power_by_lr/calculator.mbnf")
    knowledge = lr_one_parser_generator.generate()

    import pickle

    with open('knowledge.pkl', 'wb') as fd:
        pickle.dump(knowledge, fd)
