import copy

from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Productions import Productions
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.SymbolSet import SymbolSet


class FollowSet:
    def __init__(self, production: Productions, first_set):
        self.production = production
        self.first_set = first_set
        self.follow_set = {}
        self.follow_set_table = {}

    def compute(self):
        # init the follow_set
        for symbol in self.production.non_terminals:
            self.follow_set[symbol] = SymbolSet()

        self.follow_set[self.production.start_symbol] = {EOF()}

        old_follow_set = copy.deepcopy(self.follow_set)

        while True:
            for symbol in self.production:
                self.compute_symbol(symbol)

            if old_follow_set == self.follow_set:
                break
            else:
                old_follow_set = copy.deepcopy(self.follow_set)

    def compute_symbol(self, lhs_symbol):
        production_set = self.production[lhs_symbol]
        for production in production_set:
            trailer = self.follow_set[lhs_symbol]
            for rhs_symbol in reversed(production):
                if isinstance(rhs_symbol, NonTerminal):
                    self.follow_set[rhs_symbol] = self.follow_set[rhs_symbol] | trailer

                    if self.first_set[rhs_symbol].include_epsilon:
                        trailer = trailer | self.first_set[rhs_symbol].remove_epsilon()
                    else:
                        trailer = self.first_set[rhs_symbol]
                else:
                    trailer = SymbolSet({rhs_symbol})
