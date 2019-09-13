import pprint
from itertools import chain

import yaml

from MicroCompiler.ParserGenerator.Lexer import Lexer
from MicroCompiler.ParserGenerator.Parser import Parser
from MicroCompiler.Lookahead.FirstPlusSet import FirstPlusSet
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.Epsilon import Epsilon


class Generator:
    def __init__(self, input_file):
        self.translate_table = {}
        self.structure = {}

        self.input_file = input_file

    def generate(self):
        with open(self.input_file) as fd:
            bnf_string = fd.read()

        lexer = Lexer()
        lexer.parse(bnf_string)

        parser = Parser(lexer.token_list)
        parser.parse()
        productions = parser.generate_production()

        error_marker = "--"

        self.structure = {
            "terminals": [i.value for i in productions.terminals],
            "non-terminals": [i.name for i in productions.non_terminals],
            "eof-marker": "<EOF>",
            "error-marker": error_marker,
            "start-symbol": productions.start_symbol.value,
        }

        flat_productions = []
        productions_mapping = []
        for lhs_symbol in productions:
            production = productions[lhs_symbol]
            for k, v in enumerate(production):
                productions_mapping.append(frozenset({lhs_symbol.value, k}))
                flat_productions.append(
                    {
                        lhs_symbol.value: [i.value for i in v]
                        if not isinstance(v[0], Epsilon)
                        else []
                    }
                )

        self.structure["productions"] = {k: v for k, v in enumerate(flat_productions)}
        productions_mapping = {v: k for k, v in enumerate(productions_mapping)}

        fs = FirstPlusSet(productions)
        fs.compute()

        first_set_plus = fs.first_plus_set

        # for non_terminal in fs.first_plus_set:
        #     for k, v in fs.first_plus_set.items():
        #         if {non_terminal, k}

        for non_terminal in productions.non_terminals:
            for terminal in chain(productions.terminals, (EOF(),)):
                self.translate_table.setdefault(non_terminal.value, {})

                if terminal not in first_set_plus[non_terminal]:
                    # no such translation
                    self.translate_table[non_terminal.value][
                        terminal.value
                    ] = error_marker

                    continue

                inner_index = first_set_plus[non_terminal][terminal]

                look_for = frozenset({non_terminal.value, inner_index})
                if look_for not in productions_mapping:
                    raise ValueError(
                        "Terminal {} in {} not in mapping {}".format(
                            terminal, non_terminal, productions_mapping
                        )
                    )

                self.translate_table[non_terminal.value][
                    terminal.value
                ] = productions_mapping[look_for]

        self.structure["table"] = self.translate_table

        return self.structure

    def write_yaml(self, output_file):
        with open(output_file, "w") as fd:
            yaml.dump(self.structure, fd)
