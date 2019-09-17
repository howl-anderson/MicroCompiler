class Operator(object):
    def get_operand_num(self):
        raise NotImplementedError

    def eval(self, *args):
        raise NotImplementedError


class PythonBuiltinOperator(Operator):
    def __init__(self, operator, operand_num):
        self.operator = operator
        self.operand_num = operand_num

    def get_operand_num(self):
        return self.operand_num

    def eval(self, *args):
        return self.operator(*args)

    def __repr__(self):
        return "{}(operator={}, operand_num={})".format(
            self.__class__.__name__, self.operator, self.operand_num
        )
