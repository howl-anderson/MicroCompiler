import operator
from typing import Callable, List, Any

from MicroCompiler.parser_builder import ParserBuilder
from MicroCompiler.postfix_expression.operator import PythonBuiltinOperator

pb = ParserBuilder()
pb.add_generator("get_fallback_method", "fallback")
clazz = pb.generate()


class Parser(clazz):
    def __init__(self):
        self.post_expr = []

        self.method_name_mapping = {
            "(": "open_parenthesis",
            ")": "close_parenthesis",
            "/": "Division",
            "*": "Mul",
            "+": "Add",
            "-": "Sub",
            "<START>": "Start",
        }

    def fallback(self, input_):
        return input_

    def get_legal_method_name(self, method_name):
        return (
            self.method_name_mapping[method_name]
            if method_name in self.method_name_mapping
            else method_name
        )

    def get_process(self, method_name) -> Callable:
        legal_method_name = self.get_legal_method_name(method_name)
        method_func = getattr(self, legal_method_name, self.fallback)

        return method_func

    def Division(self, input_):
        return PythonBuiltinOperator(operator.truediv, 2)

    def Mul(self, input_):
        return PythonBuiltinOperator(operator.mul, 2)

    def Add(self, input_):
        return PythonBuiltinOperator(operator.add, 2)

    def Sub(self, input_):
        return PythonBuiltinOperator(operator.sub, 2)

    def num(self, input_):
        return input_.value

    def Factor(self, input_) -> List[Any]:
        if len(input_) == 1:  # Factor ->  'num'
            return [input_[0]]

        if len(input_) == 3:  # Factor -> '(' Expr ')'
            return input_[1]

    def Term(self, input_) -> List[Any]:
        if len(input_) == 1:  # Term -> Factor
            return input_[0]

        # now let us handle
        # Term -> Term '*' Factor
        #       | Term '/' Factor

        postfix_expr = []

        left_postfix_expr = input_[0]
        operator = input_[1]
        right_postfix_expr = input_[2]

        postfix_expr.extend(left_postfix_expr)
        postfix_expr.extend(right_postfix_expr)
        postfix_expr.append(operator)

        return postfix_expr

    def Expr(self, input_) -> List[Any]:
        if len(input_) == 1:  # Expr -> Term
            return input_[0]

        # now let us handle
        # Expr -> Expr '+' Term
        #       | Expr '-' Term

        postfix_expr = []

        left_postfix_expr = input_[0]
        operator = input_[1]
        right_postfix_expr = input_[2]

        postfix_expr.extend(left_postfix_expr)
        postfix_expr.extend(right_postfix_expr)
        postfix_expr.append(operator)

        return postfix_expr
