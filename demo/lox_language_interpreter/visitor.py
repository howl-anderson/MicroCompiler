from MicroCompiler.SkeletonParser import Epsilon
from MicroCompiler.interpreter.environment import Environment
from MicroCompiler.parser_builder import ParserBuilder
from MicroCompiler.postfix_expression.operator import PythonBuiltinOperator


class LoxFunction:
    def __init__(self, parameters, body):
        self.parameters = parameters
        self.body = body

    def call(self, interpreter, arguments, parent_environment):
        environment = Environment(parent_environment)
        for k, v in zip(self.parameters, arguments):
            environment.put_name(k, v)

        interpreter.execute_in_new_environment(self.body, environment)


class Interpreter:
    def __init__(self):
        self.environment = Environment()

        self.method_name_mapping = {
            "<START>": "Start",
        }

    def execute_in_new_environment(self, node, new_environment):
        original_environment = self.environment
        self.environment = new_environment
        node.access(self)
        self.environment = original_environment

    def get_method_name(self, name):
        import inspect
        method_names = [attr for attr in dir(self) if
                        inspect.ismethod(getattr(self, attr))]

        if name in self.method_name_mapping:
            name = self.method_name_mapping[name]

        if name in method_names:
            return name

        raise ValueError('Can not find correct method name for {}'.format(name))

    def num(self, input_):
        return input_.sub_node_list[0].value

    def id(self, input_):
        return input_.sub_node_list[0].value

    def AdditionalParameters(self, input_):
        parameters = []
        if len(input_.sub_node_list) > 1:
            # branch: ',' 'id' AdditionalParameters
            id_ = input_.sub_node_list[1].access(self)
            additional_id_list = input_.sub_node_list[2].access(self)

            parameters.append(id_)
            parameters.extend(additional_id_list)
        else:
            # branch: ϵ
            pass

        return parameters

    def Parameters(self, input_):
        parameters = []
        if len(input_.sub_node_list) > 1:
            # branch: 'id' AdditionalParameters
            id_ = input_.sub_node_list[0].access(self)
            additional_id_list = input_.sub_node_list[1].access(self)

            parameters.append(id_)
            parameters.extend(additional_id_list)
        else:
            # branch: ϵ
            pass

        return parameters

    def AdditionalExpressions(self, input_):
        arguments = []
        if len(input_.sub_node_list) > 1:
            # branch: ',' Expression AdditionalExpressions
            expr = input_.sub_node_list[1].access(self)
            additional_expr_list = input_.sub_node_list[2].access(self)

            arguments.append(expr)
            arguments.extend(additional_expr_list)
        else:
            # branch: ϵ
            pass

        return arguments

    def Arguments(self, input_):
        arguments = []
        if len(input_.sub_node_list) > 1:
            # branch: Expression AdditionalExpressions
            expr = input_.sub_node_list[0].access(self)
            additional_expr_list = input_.sub_node_list[1].access(self)

            arguments.append(expr)
            arguments.extend(additional_expr_list)
        else:
            # branch: ϵ
            pass

        return arguments

    def CallOrAttr(self, input_):
        return input_.sub_node_list[1].access(self)

    def Call(self, input_):
        callee = input_.sub_node_list[0].access(self)
        if isinstance(callee, str):
            func_object = self.environment.get_name(callee)
        elif isinstance(callee, LoxFunction):
            func_object = callee

        arguments = input_.sub_node_list[1].access(self)

        return func_object.call(self, arguments, self.environment)

    def Expression(self, input_):
        return input_.sub_node_list[0].access(self)

    def PrintStmt(self, input_):
        var_name = input_.sub_node_list[1].access(self)
        variable_value = self.environment.get_name(var_name)
        print(variable_value)

    def ExprStmt(self, input_):
        return input_.sub_node_list[0].access(self)

    def Statement(self, input_):
        return input_.sub_node_list[0].access(self)

    def VarDeclAssign(self, input_):
        if len(input_.sub_node_list) > 1:
            # branch: '=' Expression
            return input_.sub_node_list[1].access(self)
        else:
            # branch: ϵ
            return None

    def VarDecl(self, input_):
        var_name = input_.sub_node_list[1].access(self)
        value = input_.sub_node_list[2].access(self)
        self.environment.put_name(var_name, value)

        return None

    def Function(self, input_):
        func_name = input_.sub_node_list[0].access(self)
        parameters = input_.sub_node_list[2].access(self)
        block = input_.sub_node_list[4]
        func_object = LoxFunction(parameters, block)
        self.environment.put_name(func_name, func_object)

    def FunDecl(self, input_):
        return input_.sub_node_list[1].access(self)

    def Declaration(self, input_):
        input_.sub_node_list[0].access(self)
        return None

    def DeclarationList(self, input_):
        if len(input_.sub_node_list) > 1:
            # branch: Declaration DeclarationList
            input_.sub_node_list[0].access(self)
            input_.sub_node_list[1].access(self)
        else:
            # branch: ϵ
            pass

        return None

    def Block(self, input_):
        return input_.sub_node_list[1].access(self)

    def Primary(self, input_):
        return input_.sub_node_list[0].access(self)

    def Program(self, input_):
        return input_.sub_node_list[0].access(self)

    def Start(self, input_):
        return input_.sub_node_list[0].access(self)
