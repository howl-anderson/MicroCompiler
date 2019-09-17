from MicroCompiler.SkeletonParser import Epsilon
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

    def flat_list(self, nested_list):
        result = []

        for item in nested_list:
            if isinstance(item, list):
                flat_item = self.flat_list(item)
                result.extend(flat_item)
            else:
                result.append(item)

        return result

    def flat_nested_postfix_list(self, nested_postfix_list):
        return self.flat_list(nested_postfix_list)

    def get_legal_method_name(self, method_name):
        return (
            self.method_name_mapping[method_name]
            if method_name in self.method_name_mapping
            else method_name
        )

    def Division(self, input_):
        return PythonBuiltinOperator(input_[0], 2)

    def Mul(self, input_):
        return PythonBuiltinOperator(input_[0], 2)

    def Add(self, input_):
        return PythonBuiltinOperator(input_[0], 2)

    def Sub(self, input_):
        return PythonBuiltinOperator(input_[0], 2)

    def num(self, input_):
        return input_[0]

    def ExprTwo(self, input_):
        # ExprTwo -> '+' Term ExprTwo
        #          | '-' Term ExprTwo
        #          | ϵ ;

        if len(input_) == 1:
            # ExprTwo -> ϵ
            return Epsilon()

        if isinstance(input_[2], Epsilon):
            # ExprTwo -> '+' Term ExprTwo | '-' Term ExprTwo
            #                        |                  |
            #                        -> ϵ               -> ϵ
            return [input_[0], [input_[1]]]

        if isinstance(input_[2], list):
            # ExprTwo -> '+' Term ExprTwo | '-' Term ExprTwo
            #                        |                  |
            #                        -> ['+' num]       -> ['-' num]

            postfix_expr = input_[2][1]

            postfix_expr = postfix_expr[:]  # shallow copy

            head = postfix_expr.pop(0)
            operator = input_[2][0]

            postfix_expr.insert(0, operator)
            postfix_expr.insert(0, head)
            postfix_expr.insert(0, input_[1])

            return [input_[0], postfix_expr]

    def TermTwo(self, input_):
        # TermTwo -> '*' Factor TermTwo
        #          | '/' Factor TermTwo
        #          | ϵ ;

        if len(input_) == 1:
            # ExprTwo -> ϵ
            return Epsilon()

        if isinstance(input_[2], Epsilon):
            # ExprTwo -> '+' Factor TermTwo | '-' Factor TermTwo
            #                          |                   |
            #                          -> ϵ                -> ϵ
            #
            # output:  ['*', postfix_expr]
            #                |----------|
            #                 type: list

            return [input_[0], [input_[1]]]

        if isinstance(input_[2], list):
            # TermTwo -> '*' Factor TermTwo | '/' Factor TermTwo
            #                         |                    |
            #                         -> ['/' num]          -> ['*' num]

            # input_: ['*', Factor, ['/', [head, rest_of_postfix_expr]]]
            #                             |---------------------------|
            #                                post_expr (type: list)
            #
            # output: ['*', [Factor, head, '/', rest_of_postfix_expr]]

            postfix_expr = input_[2][1]

            postfix_expr = postfix_expr[:]  # shallow copy

            head = postfix_expr.pop(0)
            operator = input_[2][0]

            postfix_expr.insert(0, operator)
            postfix_expr.insert(0, head)
            postfix_expr.insert(0, input_[1])

            return [input_[0], postfix_expr]

    def Factor(self, input_):
        if len(input_) == 1:
            return input_[0]

        if len(input_) == 3:
            return input_[1]

    def Term(self, input_):
        if isinstance(input_[1], Epsilon):
            # Term -> Factor TermTwo ;
            #                  |
            #                  -> ϵ
            return input_[0]

        # Term -> Factor TermTwo ;
        #                   |
        #                   -> ['*', postfix_expr]

        # input_: [Factor, ['/', [head, rest_of_postfix_expr]]]
        #                        |---------------------------|
        #                            post_expr (type: list)
        #
        # output: [Factor, head, '/', rest_of_postfix_expr]

        postfix_expr = input_[1][1]

        postfix_expr = postfix_expr[:]  # shallow copy

        head = postfix_expr.pop(0)
        operator = input_[1][0]

        postfix_expr.insert(0, operator)
        postfix_expr.insert(0, head)
        postfix_expr.insert(0, input_[0])

        return postfix_expr

    def Expr(self, input_):
        if isinstance(input_[1], Epsilon):
            # Expr -> Term ExprTwo ;
            #                |
            #                -> ϵ
            return input_[0]

        # Expr -> Term ExprTwo ;
        #                |
        #                -> [operator, postfix_expr]

        # input_: [Factor, ['/', [head, rest_of_postfix_expr]]]
        #                        |---------------------------|
        #                            post_expr (type: list)
        #
        # output: [Factor, head, '/', rest_of_postfix_expr]
        postfix_expr = input_[1][1]

        postfix_expr = postfix_expr[:]  # shallow copy

        head = postfix_expr.pop(0)

        operator = input_[1][0]

        postfix_expr.insert(0, operator)
        postfix_expr.insert(0, head)
        postfix_expr.insert(0, input_[0])

        return postfix_expr

    def Goal(self, input_):
        expr = input_[0]
        flat_postfix_expr = self.flat_nested_postfix_list(expr)

        return flat_postfix_expr

    def Start(self, input_):
        return input_[0]
