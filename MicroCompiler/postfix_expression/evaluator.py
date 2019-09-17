from MicroCompiler.postfix_expression.operator import Operator


class Evaluator(object):
    def __init__(self, post_expr):
        self.post_expr = post_expr

        self.value_stack = []

    def eval(self):
        for expr in self.post_expr:
            if isinstance(expr, Operator):  # this is an operator
                args = self.pop_top_k_value(expr.get_operand_num())
                value = expr.eval(*args)
                self.value_stack.append(value)
            else:  # this is an operand
                self.value_stack.append(expr)

        assert len(self.value_stack) == 1

        return self.value_stack[0]

    def pop_top_k_value(self, k):
        args = []
        for _ in range(k):
            args.insert(0, self.value_stack.pop())

        return args
