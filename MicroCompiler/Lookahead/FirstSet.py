import copy

from MicroCompiler.Productions import Productions
from MicroCompiler.Lookahead.SymbolSet import SymbolSet


class FirstSet:
    def __init__(self, production: Productions):
        self.first_set = {}
        self.first_set_table = {}
        self.first_set_mapping = {}
        self.production = production

    def compute(self):
        # compute all terminal's first-set first
        for symbol in self.production.terminals:
            self.first_set[symbol] = SymbolSet({symbol})

        epsilon = self.production.epsilon
        self.first_set[epsilon] = SymbolSet({epsilon})

        eof = self.production.eof
        self.first_set[eof] = SymbolSet({eof})

        # init non-terminal's first-set to empty
        for symbol in self.production.non_terminals:
            self.first_set[symbol] = SymbolSet()

        old_first_set = copy.deepcopy(self.first_set)

        while True:
            for symbol in self.production.non_terminals:
                self.compute_symbol(symbol)
            if self.first_set == old_first_set:
                break
            else:
                old_first_set = copy.deepcopy(self.first_set)

    def compute_symbol(self, lsh_symbol):
        productions = self.production[lsh_symbol]

        for production_index, production in enumerate(productions):
            rhs = SymbolSet()
            for symbol_index, rhs_symbol in enumerate(production):
                if symbol_index != len(production) - 1:
                    rhs.update(self.first_set[rhs_symbol].remove_epsilon())
                else:
                    # keep epsilon if this is the last symbol in the production
                    rhs.update(self.first_set[rhs_symbol])

                if not self.first_set[rhs_symbol].include_epsilon:
                    break

            self.first_set[lsh_symbol].update(rhs)

            self.first_set_mapping.setdefault(lsh_symbol, {})
            self.first_set_mapping[lsh_symbol][production_index] = rhs
