import unittest

from MicroCompiler.Productions import Productions
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import CHARACTER
from MicroCompiler.Lookahead.Terminal import Terminal


class TestProduction(unittest.TestCase):
    def test_conception(self):
        statement = NonTerminal("Statement")
        expression = NonTerminal("Expression")
        semicolon = Terminal(CHARACTER, ";")
        production = Productions({
            statement: [
                [expression, semicolon]
            ]
        })

        production.print_as_bnf()

        self.assertEqual(production.terminals, {semicolon})
        self.assertEqual(production.non_terminals, {statement, expression})
