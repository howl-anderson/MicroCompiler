class ReduceError(Exception):
    pass


class ShiftReduceParser(object):
    def __init__(self, tokens):
        self.tokens = tokens

        self.stack = []  # a list of [stack_bottom, ...,  stack_top]
        # the unconsumed token on the right side
        self.queue = []

        # initial queue with tokens
        self.queue.extend(self.tokens[:])

    def shift(self):
        token = self.queue.pop(0)
        self.stack.append(token)

    def get_stack_top(self):
        return self.stack[-1]

    def is_accepted(self):
        pass

    def reduce(self, lhs, rhs):
        stack_tops = self.tokens[-len(rhs) :]
        if stack_tops != rhs:
            raise ReduceError()

        # remove stack tops
        self.tokens = self.tokens[: -len(rhs)]

        # push new element
        self.tokens.append(lhs)
