from MicroCompiler.cfg import Terminal, NonTerminal


class BaseInstance:
    index_counter = 0

    def __init__(self):
        self.index = self.index_counter

        self.increase_index_counter()

    @classmethod
    def increase_index_counter(cls):
        cls.index_counter += 1


class NonTerminalInstance(BaseInstance):
    def __init__(self, name):
        self.name = name

        super().__init__()

    @property
    def value(self):
        return self.name

    @classmethod
    def convert_from(cls, obj: NonTerminal):
        if isinstance(obj, cls):
            return obj
        else:
            instance = cls(obj.name)

            return instance


class TerminalInstance(BaseInstance):
    def __init__(self, type, token):
        self.type = type

        self.token = token

        super().__init__()

    @property
    def value(self):
        return self.type

    @classmethod
    def convert_from(cls, obj: Terminal):
        if isinstance(obj, cls):
            return obj
        else:
            instance = cls(obj.type, obj.token)

            return instance


class Instance:
    @classmethod
    def convert_from(cls, obj):
        if isinstance(obj, Terminal):
            return TerminalInstance.convert_from(obj)
        else:
            return NonTerminalInstance.convert_from(obj)
