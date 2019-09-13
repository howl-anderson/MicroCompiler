import yaml


class SkeletonSyntaxError(Exception):
    pass


class SkeletonParser:
    def __init__(self, definition_file, lexeme_list):
        definition_file = definition_file
        self.lexeme_list = lexeme_list
        self.lexeme_index = 0

        with open(definition_file) as fd:
            definition = yaml.load(fd.read())

        self.start_symbol = definition["start-symbol"]
        self.error_marker = definition["error-marker"]
        self.productions = definition["productions"]
        self.table = definition["table"]
        self.terminals = definition["terminals"]
        self.non_terminals = definition["non-terminals"]
        self.eof_marker = definition["eof-marker"]

    def parse(self):
        result = False
        try:
            result = self.parse_symbol(self.start_symbol)
        except SkeletonSyntaxError as e:
            print(e)
        finally:
            if result:
                print("SUCCESS")
                return True
            else:
                print("FAILED")
                return False

    def parse_symbol(self, symbol):
        if symbol in self.terminals:
            self.lexeme_index += 1
            return True

        if symbol not in self.table:
            raise SkeletonSyntaxError("Symbol: {} not in {}".format(symbol, self.table))

        lookahead_symbol = self.lexeme_list[self.lexeme_index]
        if lookahead_symbol not in self.table[symbol]:
            raise SkeletonSyntaxError(
                "Lookahead symbol: {} not in {}".format(
                    lookahead_symbol, self.table[symbol]
                )
            )

        predict_indicator = self.table[symbol][lookahead_symbol]

        if predict_indicator == self.error_marker:
            raise SkeletonSyntaxError(
                "Invalid lookahead symbol: {} in {}".format(lookahead_symbol, symbol)
            )

        if predict_indicator not in self.productions:
            raise SkeletonSyntaxError("{} not in {}")

        production = list(self.productions[predict_indicator].values())[0]
        if not len(production):
            return True

        result_list = []
        for i in production:
            result_list.append(self.parse_symbol(i))

        if all(result_list):
            return True
        return False
