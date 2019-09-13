from MicroCompiler.Lookahead.FirstSet import FirstSet
from MicroCompiler.Lookahead.FollowSet import FollowSet


class FirstPlusSet:
    def __init__(self, production):
        self.first_set = None
        self.follow_set = None
        self.first_set_mapping = None
        self.production = production

        self.first_plus_set = {}
        self.first_plus_set_mapping = {}

    def compute(self):
        if self.first_set is None:
            fs = FirstSet(self.production)
            fs.compute()
            self.first_set = fs.first_set
            self.first_set_mapping = fs.first_set_mapping

        if self.follow_set is None:
            fs = FollowSet(self.production, self.first_set)
            fs.compute()
            self.follow_set = fs.follow_set

        for lhs_symbol in self.production:
            productions = self.production[lhs_symbol]
            for production_index, production in enumerate(productions):
                symbol_set = self.first_set_mapping[lhs_symbol][production_index]

                self.first_plus_set_mapping.setdefault(lhs_symbol, {})
                self.first_plus_set_mapping[lhs_symbol].setdefault(
                    production_index, set()
                )
                first_plus_set = self.first_plus_set_mapping[lhs_symbol][
                    production_index
                ]
                if symbol_set.include_epsilon:
                    first_plus_set.update(symbol_set.remove_epsilon())
                    first_plus_set.update(self.follow_set[lhs_symbol])
                else:
                    first_plus_set.update(symbol_set)

                self.first_plus_set.setdefault(lhs_symbol, {})
                for symbol in first_plus_set:
                    if symbol in self.first_plus_set[lhs_symbol]:
                        msg = "Lookahead {} index {} already exists in {}"
                        raise ValueError(
                            msg.format(
                                symbol,
                                production_index,
                                self.first_plus_set[lhs_symbol],
                            )
                        )
                    self.first_plus_set[lhs_symbol][symbol] = production_index
