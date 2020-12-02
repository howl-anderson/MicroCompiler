from MicroCompiler.parser_builder import ParserBuilder

pb = ParserBuilder()
pb.add_generator("get_fallback_method", "fallback")
clazz = pb.generate()


class Parser(clazz):
    def __init__(self, data: dict):
        self.method_name_mapping = {
            "<START>": "Start",
        }
        self.data = data

    def fallback(self, input_):
        return ""

    def get_legal_method_name(self, method_name):
        return (
            self.method_name_mapping[method_name]
            if method_name in self.method_name_mapping
            else method_name
        )

    def const(self, input_):
        return input_[0]

    def var(self, input_):
        key = input_[0]
        return self.data[key]

    def VarBlock(self, input_):
        return input_[1]

    def Block(self, input_):
        return input_[0]

    def TermPlus(self, input_):
        if len(input_) == 1:
            return ""
        else:
            return "".join(input_)

    def Term(self, input_):
        return input_[0]

    def Expr(self, input_):
        if len(input_) == 1:
            return ""
        else:
            return "".join(input_)

    def Goal(self, input_):
        return input_[0]

    def Start(self, input_):
        return input_[0]
