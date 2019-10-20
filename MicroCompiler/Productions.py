from typing import List, Mapping, Union

from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.Lookahead.Epsilon import Epsilon
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.NonTerminal import NonTerminal


class Productions(dict):
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

    def print_as_bnf(self):
        for lhs_symbol in self:
            print(lhs_symbol, " ->")
            rhs_symbol = self[lhs_symbol]
            production_str_list = []
            for production in rhs_symbol:
                production_str_list.append(" ".join([str(i) for i in production]))
            print("    ", " | ".join(production_str_list))
            print(";")
