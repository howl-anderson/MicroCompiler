class BaseToken:
    index_counter = 0

    def __init__(self, type: str, value=None):
        self.type = type
        self.value = value

        self.index = self.index_counter

        self.increase_index_counter()

    @classmethod
    def increase_index_counter(cls):
        cls.index_counter += 1
