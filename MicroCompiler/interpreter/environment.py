class VariableNameNotFound(ValueError):
    pass


class Environment(object):
    def __init__(self, closure=None):
        self.closure = closure
        self.data = {}

    def put_name(self, name, value):
        # overwrite is allowed
        self.data[name] = value

    def get_name(self, name):
        if name in self.data:
            return self.data[name]

        if self.closure:
            return self.closure.get_name(name)

        return VariableNameNotFound("Can not find variable: {}".format(name))
