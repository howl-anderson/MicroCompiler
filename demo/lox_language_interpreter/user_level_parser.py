from MicroCompiler.SkeletonParser import Epsilon
from MicroCompiler.interpreter.environment import Environment
from MicroCompiler.parser_builder import ParserBuilder
from MicroCompiler.postfix_expression.operator import PythonBuiltinOperator

pb = ParserBuilder()
pb.add_generator("get_fallback_method", "fallback")
clazz = pb.generate()


class Parser(clazz):
    def __init__(self):
        self.environment = Environment()

        self.method_name_mapping = {
            "<START>": "Start",
        }

    def fallback(self, input_):
        return input_

    def num(self, input_):
        return input_[0].value

    def Expr(self, input_):
        return input_[0]

    def StateList(self, input_):
        if len(input_) > 1:
            # branch: State ';' StateList
            pass
        else:
            # branch: ϵ
            pass

        return None

    def State(self, input_):
        if len(input_) > 2:
            # branch: 'var' 'id' '=' Expr
            self.environment.put_name(input_[1].value, input_[3])
        else:
            # branch: 'print' 'id'
            variable_value = self.environment.get_name(input_[1].value)
            print(variable_value)

        return None

    def Goal(self, input_):
        return input_[0]

    def Start(self, input_):
        return input_[0]
