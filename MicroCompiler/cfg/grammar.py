import os
from typing import List, Mapping, Union

from jinja2 import Environment
from jinja2 import FileSystemLoader

from MicroCompiler.cfg.terminal import Terminal
from MicroCompiler.cfg.epsilon import Epsilon
from MicroCompiler.cfg.non_terminal import NonTerminal
from MicroCompiler.Lookahead.EOF import EOF

current_path = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_path, 'templates')

jinja2_env = Environment(loader=FileSystemLoader(template_dir),
                         trim_blocks=False)


class Grammar(dict):
    epsilon = Epsilon()
    eof = EOF()

    def __init__(self, *args, **kwargs):
        self._elements = set()
        self._terminals = set()
        self._non_terminals = set()
        self.start_symbol = None  # type: NonTerminal

        super().__init__(*args, **kwargs)

    def set_start_symbol(self, start_symbol):
        if start_symbol not in self:
            raise ValueError("start symbol must in production.")
        self.start_symbol = start_symbol

    def get_all_elements(self, without_start_symbol=True):
        if not without_start_symbol:
            return self._elements
        else:
            return self._elements - {self.start_symbol, }

    def get_all_non_terminals(self, without_start_symbol=True):
        if not without_start_symbol:
            return self._non_terminals
        else:
            return self._non_terminals - {self.start_symbol, }

    def compute_elements(self):
        for non_terminal in self:
            self._elements.add(non_terminal)
            productions = self[non_terminal]
            for production in productions:
                for element in production:
                    self._elements.add(element)

        self._terminals = {i for i in self._elements if isinstance(i, Terminal)}
        self._non_terminals = {i for i in self._elements if isinstance(i, NonTerminal)}

    @property
    def terminals(self):
        self.compute_elements()
        return {i for i in self._terminals}

    @property
    def non_terminals(self):
        self.compute_elements()
        return {i for i in self._non_terminals}

    def _generate_production_mbnf(self, lhs_symbol) -> str:
        rhs = self[lhs_symbol]

        template = jinja2_env.get_template('grammar.jinja2')
        result = template.render(lhs=lhs_symbol, rhs=rhs)
        return result

    def render_as_mbnf(self) -> str:
        output_list = []
        for lhs_symbol in self:
            result = self._generate_production_mbnf(lhs_symbol)
            output_list.append(result)

        return "\n".join(output_list)

    def print_as_bnf(self):
        production_str_list = []
        for lhs_symbol in self:
            production_str = ""
            print(lhs_symbol, " ->")
            rhs_symbol = self[lhs_symbol]
            production_str_list = []
            for production in rhs_symbol:
                production_str_list.append(" ".join([str(i) for i in production]))
            print("    ", " | ".join(production_str_list))
            print(";")

    def write_to_file(self, grammar_file):
        mbnf_string = self.render_as_mbnf()
        with open(grammar_file, 'wt') as fd:
            fd.write(mbnf_string)

