import copy
from typing import List, Union

from MicroCompiler.cfg import Epsilon
from MicroCompiler.cfg import NonTerminal
from MicroCompiler.cfg import Terminal


class RightHandSide(object):
    def __init__(
        self, symbols: List[Union[Terminal, NonTerminal]], placeholder_offset=0
    ):
        if len(symbols) == 1 and isinstance(symbols[0], Epsilon):
            # The only LR(0) item for X → ε is X → •
            self.symbols = []
        else:
            self.symbols = symbols

        self.placeholder_offset = placeholder_offset  # AKA the . offset
        self.placeholder_symbol = "•"

    def get_symbol_around_mark(self, offset=1):
        index_offset = offset - 1 if offset > 0 else offset
        offset = self.placeholder_offset + index_offset

        if offset >= len(self.symbols):
            return None
        else:
            return self.symbols[self.placeholder_offset + index_offset]

    def get_symbols_around_mask_to_tail(self, offset=2):
        index_offset = offset - 1 if offset > 0 else offset
        return self.symbols[self.placeholder_offset + index_offset :]

    def is_mark_at_end(self):
        return self.placeholder_offset == len(self.symbols)

    def forward_mask(self) -> bool:
        if self.placeholder_offset >= len(self.symbols):
            return False

        self.placeholder_offset += 1

        return True

    def __len__(self):
        return len(self.symbols)

    def __deepcopy__(self, memodict={}):
        return self.__class__(
            symbols=copy.deepcopy(self.symbols),
            placeholder_offset=copy.deepcopy(self.placeholder_offset),
        )

    def __str__(self):
        return "{!s} {} {!s}".format(
            " ".join([str(i) for i in self.symbols[: self.placeholder_offset]]),
            self.placeholder_symbol,
            " ".join([str(i) for i in self.symbols[self.placeholder_offset :]]),
        )

    def __repr__(self):
        return "{}({}, {})".format(
            self.__class__.__name__, self.symbols, self.placeholder_offset
        )

    def __hash__(self):
        return hash((frozenset(enumerate(self.symbols)), self.placeholder_offset))

    def __eq__(self, other):
        return (
            self.symbols == other.symbols
            and self.placeholder_offset == other.placeholder_offset
        )
