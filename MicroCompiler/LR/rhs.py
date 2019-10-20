import copy
from typing import List, Union

from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import Terminal


class RightHandSide(object):
    def __init__(self, symbols: List[Union[Terminal, NonTerminal]], mark_offset=0):
        self.symbols = symbols
        self.mark_offset = mark_offset  # AKA the . offset
        self.mark_symbol = "•"

    def get_symbol_around_mark(self, offset=1):
        index_offset = offset - 1 if offset > 0 else offset
        offset = self.mark_offset + index_offset

        if offset >= len(self.symbols):
            return None
        else:
            return self.symbols[self.mark_offset + index_offset]

    def get_symbols_around_mask_to_tail(self, offset=2):
        index_offset = offset - 1 if offset > 0 else offset
        return self.symbols[self.mark_offset + index_offset :]

    def is_mark_at_end(self):
        return self.mark_offset == len(self.symbols)

    def forward_mask(self) -> bool:
        if self.mark_offset >= len(self.symbols):
            return False

        self.mark_offset += 1

        return True

    def __len__(self):
        return len(self.symbols)

    def __deepcopy__(self, memodict={}):
        return self.__class__(
            symbols=copy.deepcopy(self.symbols),
            mark_offset=copy.deepcopy(self.mark_offset),
        )

    def __str__(self):
        return "{!s} {} {!s}".format(
            " ".join([str(i) for i in self.symbols[: self.mark_offset]]),
            self.mark_symbol,
            " ".join([str(i) for i in self.symbols[self.mark_offset :]]),
        )

    def __repr__(self):
        return "{}({}, {})".format(
            self.__class__.__name__, self.symbols, self.mark_offset
        )

    def __hash__(self):
        return hash((frozenset(enumerate(self.symbols)), self.mark_offset))

    def __eq__(self, other):
        return self.symbols == other.symbols and self.mark_offset == other.mark_offset
