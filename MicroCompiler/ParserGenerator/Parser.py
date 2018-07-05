from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.Lookahead.Epsilon import Epsilon
from MicroCompiler.Productions import Productions
from MicroCompiler.Lookahead.EOF import EOF
from .Lexeme import (
    NON_TERMINAL,
    TERMINAL,
    PRODUCT,
    ALTERNATIVE,
    SEMICOLON,
    EPSILON
)


built_in_terminal = (
)

# filter function list
terminal_filter_list = (
)


class Parser:
    def __init__(self, token_list):
        self.token_index = 0
        self.token_list = token_list

        self.production_dict = {}
        self.start_symbol = None

        super().__init__()

    def _match(self, value):
        if self.token_list[self.token_index].type_ == TERMINAL and self.token_list[self.token_index] == value:
            self.token_index += 1
            return True
        else:
            # print("{} != {}".format(self.token_list[self.token_index], value))
            return False

    def _match_type(self, type_):
        if self.token_list[self.token_index].type_ == type_:
            self.token_index += 1
            return True
        else:
            # print("{} != {}".format(self.token_list[self.token_index], type))
            return False

    def _non_terminal(self):
        if self.token_index >= len(self.token_list):
            return False

        if self.token_list[self.token_index].type_ == NON_TERMINAL:
            self.token_index += 1
            return True
        else:
            # print("{} is not NON_TERMINAL".format(self.token_list[self.token_index]))
            return False

    def _terminal(self):
        if self.token_list[self.token_index].type_ == TERMINAL:
            self.token_index += 1
            return True
        else:
            # print("{} is not TERMINAL".format(self.token_list[self.token_index]))
            return False

    """
    statement -> production ';' other_production ;
    other_production -> statement | ϵ ;

    production -> non_terminal '->' symbols other_symbols ;
    other_symbols -> '|' symbols other_symbols | ϵ ;

    symbols -> symbol other_symbol | 'ϵ' ;
    other_symbol -> symbol other_symbol | ϵ ;

    symbol -> non_terminal | terminal ;
    """
    def parse(self):
        return self._statement()

    def _statement(self):
        return self._production() and self._match_type(SEMICOLON) and self._other_production()

    def _other_production(self):
        save_point = self.token_index
        if self._statement():
            return True
        else:
            self.token_index = save_point
            # do nothing for epsilon
            return True

    def _production(self):
        save_point = self.token_index
        if self._non_terminal():
            productions_object = []

            # first non_terminal is start symbol
            if not self.production_dict:
                self.start_symbol = self.token_list[save_point]

            self.production_dict[self.token_list[save_point]] = productions_object

            return self._match_type(PRODUCT) and self._symbols(productions_object) and self._other_symbols(productions_object)
        else:
            return False

    def _other_symbols(self, productions_object):
        save_point = self.token_index
        if self._match_type(ALTERNATIVE) and self._symbols(productions_object) and self._other_symbols(productions_object):
            return True
        else:
            self.token_index = save_point
            # do nothing for epsilon
            return True

    def _symbols(self, productions_object):
        save_point = self.token_index

        production = []
        result = self._symbol(production) and self._other_symbol(production)

        if result:
            productions_object.append(production)

        if not result:
            if self._match_type(EPSILON):
                productions_object.append([self.token_list[save_point]])
                return True
            return False
        return True

    def _other_symbol(self, production):
        save_point = self.token_index
        if self._symbol(production) and self._other_symbol(production):
            return True
        else:
            self.token_index = save_point
            # do nothing for epsilon
            return True

    def _symbol(self, production):
        save_point = self.token_index
        if self._non_terminal():
            production.append(self.token_list[save_point])
            return True
        else:
            self.token_index = save_point
            result = self._terminal()

            if result:
                production.append(self.token_list[save_point])
            return result

    def generate_production(self):
        formal_production = Productions()

        for lhs_lexeme in self.production_dict:
            lhs_symbol = NonTerminal(lhs_lexeme.value)
            production_list = []
            formal_production[lhs_symbol] = production_list

            if lhs_lexeme == self.start_symbol:
                formal_production.start_symbol = lhs_symbol

            productions = self.production_dict[lhs_lexeme]
            for production in productions:
                production_symbols = []
                production_list.append(production_symbols)
                for rhs_symbol in production:
                    if rhs_symbol.type_ == EPSILON:
                        production_symbols.append(Epsilon())
                    elif rhs_symbol.type_ == NON_TERMINAL:
                        production_symbols.append(NonTerminal(rhs_symbol.value))
                    elif rhs_symbol.type_ == TERMINAL:
                        production_symbols.append(Terminal(type_=None, data=rhs_symbol.value))

        return formal_production
