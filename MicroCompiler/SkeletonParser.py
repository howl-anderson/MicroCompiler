import yaml


class SkeletonSyntaxError(Exception):
    pass


class Token(object):
    index_counter = 0

    def __init__(self, type_, value=None, index=None):
        self.type = type_
        self.value = value
        self.index = index if index else self.index_counter

        self.increase_index_counter()

    @classmethod
    def increase_index_counter(cls):
        cls.index_counter += 1

    def __repr__(self):
        return "{}(type_={}, value={}，index={})".format(
            self.__class__.__name__, self.type, self.value, self.index
        )


class WhiteSpaceToken(Token):
    index_counter = 0

    def __init__(self, value=None, index=None):
        super(WhiteSpaceToken, self).__init__(type_='white_space', value=value, index=index)


class Epsilon(object):
    def __repr__(self):
        return "Epsilon()"


class Node(object):
    index_counter = 0

    def __init__(self, type_, value=None, index=None):
        self.type = type_
        self.value = value
        self.index = index if index else self.index_counter

        self.increase_index_counter()

    @classmethod
    def increase_index_counter(cls):
        cls.index_counter += 1

    def __repr__(self):
        return "{}(type_={}, value={}，index={})".format(
            self.__class__.__name__, self.type, self.value, self.index
        )


class SkeletonParser:
    def __init__(self, definition_file, lexeme_list):
        definition_file = definition_file
        self.lexeme_list = lexeme_list
        self.lexeme_index = 0

        with open(definition_file) as fd:
            definition = yaml.load(fd.read(), Loader=yaml.FullLoader)

        self.start_symbol = definition["start-symbol"]
        self.error_marker = definition["error-marker"]
        self.productions = definition["productions"]
        self.table = definition["table"]
        self.terminals = definition["terminals"]
        self.non_terminals = definition["non-terminals"]
        self.eof_marker = definition["eof-marker"]

        # debug
        self.token_stack = []
        self.call_stack = []

    def parse(self):
        previous_symbol = Node("<START>")
        start_symbol = Node(self.start_symbol)
        result = self.parse_symbol(start_symbol, previous_symbol)

        if result:
            return True
        else:
            return False

    def call_parser_method(self, parser):
        value_stack = []
        for symbol in self.call_stack.pop():
            method = getattr(parser, symbol)
            value = value_stack.pop()
            return_value = method(value)
            value_stack.append(return_value)

    def parse_symbol(self, symbol, previous_symbol):
        self.token_stack.append(self.lexeme_list[self.lexeme_index])
        self.call_stack.append((previous_symbol, symbol))

        if symbol.type in self.terminals:

            lexeme = self.lexeme_list[self.lexeme_index]

            self.call_stack.append((symbol, lexeme))
            self.token_stack.append(lexeme)

            self.lexeme_index += 1

            return True

        if symbol.type not in self.table:
            raise SkeletonSyntaxError(
                "Symbol: {} not in {}".format(symbol.type, self.table)
            )

        lookahead_symbol = self.lexeme_list[self.lexeme_index]
        if lookahead_symbol.type not in self.table[symbol.type]:
            raise SkeletonSyntaxError(
                "Lookahead symbol: {} not in {}".format(
                    lookahead_symbol.type, self.table[symbol.type]
                )
            )

        predict_indicator = self.table[symbol.type][lookahead_symbol.type]

        if predict_indicator == self.error_marker:
            raise SkeletonSyntaxError(
                "Invalid lookahead symbol: {} in {}".format(
                    lookahead_symbol.type, symbol.type
                )
            )

        if predict_indicator not in self.productions:
            raise SkeletonSyntaxError("{} not in {}")

        production = list(self.productions[predict_indicator].values())[0]
        if not len(production):
            self.call_stack.append((symbol, Token("ϵ", Epsilon())))
            self.token_stack.append(Token("ϵ"))

            return True

        result_list = []
        for i in production:
            next_symbol = Node(i)
            result_list.append(self.parse_symbol(next_symbol, symbol))

        if all(result_list):
            return True
        return False
