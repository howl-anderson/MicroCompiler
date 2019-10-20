from typing import FrozenSet, Set, Mapping

from MicroCompiler.LR.lr_one_item import LR1Item

global_state_registry: Mapping['State', int] = {}


class State(Set[LR1Item]):
    id_counter = 0

    def __init__(self, *args, **kwargs):
        super(State, self).__init__(*args, **kwargs)

        self.id = None

    @classmethod
    def get_id(cls):
        id_ = cls.id_counter
        cls.id_counter += 1

        return id_

    def setup_id(self):
        if self in global_state_registry:
            self.id = global_state_registry[self]

        if self.id is None:
            self.id = self.get_id()
            global_state_registry[self] = self.id

    def __repr__(self):
        return "{}#{}".format(self.__class__.__name__, self.id)

    def __hash__(self):
        return hash(frozenset(self))

    def __eq__(self, other):
        return frozenset(self) == frozenset(other)


if __name__ == "__main__":
    state1 = State([1, 2])
    print(state1)

    state2 = State([1, 2])
    print(state2)

    assert not (state1 == state2)
