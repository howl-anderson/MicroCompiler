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

    def baa(self, input_) -> int:
        return 1

    def SheepNoise(self, input_) -> int:
        if len(input_) == 1:  # SheepNoise ->  'baa'
            return input_[0]

        if len(input_) == 2:  # SheepNoise -> SheepNoise 'baa'
            return input_[0] + input_[1]
