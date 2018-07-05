class EOF:
    def __str__(self):
        return "<EOF>"

    @property
    def value(self):
        return '<EOF>'

    def __hash__(self):
        return hash('<EOF>')

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return True

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)