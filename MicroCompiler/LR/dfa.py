class DFA(object):
    def __init__(self, start_status=None):
        self.start = start_status
        self.table = {}

        self.current_status = self.start

    def match_one_symbol(self, symbol, from_status=None):
        # default current status is load from global variable
        current_status = self.current_status
        if from_status is not None:
            current_status = from_status

        if current_status in self.table:
            status_lookup_table = self.table[current_status]
            if symbol in status_lookup_table:
                self.current_status = status_lookup_table[symbol]
                return self.current_status
            else:
                # this symbol goes nowhere
                return None
        else:
            # this status goes nowhere
            return None

    def get_status_lookup_table(self, status):
        return self.table[self.current_status]
