import types


class ParserBuilder(object):
    def __init__(self, parser_name="ParserClass"):
        self.parser_name = parser_name
        self.generators = dict()

    def add_generator(self, from_statement, to_statements):
        def generator(self, to_statements=to_statements):
            print(to_statements)
            # raise NotImplementedError

        self.generators[from_statement] = generator

    def generate(self):
        return type(self.parser_name, (), self.generators)


if __name__ == "__main__":
    pb = ParserBuilder()
    pb.add_generator('some_method', 'Who Am I')
    clazz = pb.generate()
    i = clazz()
    print(i.some_method())
    print("")
