import unittest
import pprint

from MicroCompiler.Productions import Productions
from MicroCompiler.Lookahead.Epsilon import Epsilon
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.FirstPlusSet import FirstPlusSet
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import CHARACTER
from MicroCompiler.Lookahead.Terminal import Terminal


class TestFirstPlusSet(unittest.TestCase):
    def test_conception(self):
        statement = NonTerminal("Statement")
        expression = NonTerminal("Expression")
        semicolon = Terminal(CHARACTER, ";")
        plus = Terminal(CHARACTER, "+")
        minus = Terminal(CHARACTER, "-")

        production = Productions(
            {statement: [[expression, semicolon]], expression: [[plus], [minus]]}
        )

        production.set_start_symbol(statement)

        fs = FirstPlusSet(production)
        fs.compute()

        real_result = fs.first_plus_set

        expect_result = {
            NonTerminal("Expression"): {
                Terminal(CHARACTER, "+"): 0,
                Terminal(CHARACTER, "-"): 1,
            },
            NonTerminal("Statement"): {
                Terminal(CHARACTER, "+"): 0,
                Terminal(CHARACTER, "-"): 0,
            },
        }

        self.assertEqual(real_result, expect_result)

    def test_epsilon(self):
        statement = NonTerminal("Statement")
        expression = NonTerminal("Expression")
        epsilon = Epsilon()
        semicolon = Terminal(CHARACTER, ";")
        plus = Terminal(CHARACTER, "+")
        minus = Terminal(CHARACTER, "-")

        production = Productions(
            {
                statement: [[expression, semicolon]],
                expression: [[plus], [minus], [epsilon]],
            }
        )

        production.set_start_symbol(statement)

        fs = FirstPlusSet(production)
        fs.compute()

        real_result = fs.first_plus_set

        expect_result = {
            NonTerminal("Statement"): {
                Terminal(CHARACTER, "+"): 0,
                Terminal(CHARACTER, "-"): 0,
                Terminal(CHARACTER, ";"): 0,
            },
            NonTerminal("Expression"): {
                Terminal(CHARACTER, "+"): 0,
                Terminal(CHARACTER, "-"): 1,
                Terminal(CHARACTER, ";"): 2,
            },
        }

        self.assertEqual(real_result, expect_result)

    def test_real(self):
        """
        Goal -> Expr ;
        Expr -> Term ExprTwo ;
        ExprTwo -> '+' Term ExprTwo
                 | '-' Term ExprTwo
                 | ϵ ;
        Term -> Factor TermTwo ;
        TermTwo -> '*' Factor TermTwo
                 | '/' Factor TermTwo
                 | ϵ ;
        Factor -> '(' Expr ')'
                | 'num'
                | 'name' ;
        """

        """
        Extended Backus-Naur form:

        Goal -> Expr
        Expr -> Term ExprTwo
        ExprTwo -> + Term ExprTwo | - Term ExprTwo | EPSILON
        Term -> Factor TermTwo
        TermTwo -> * Factor TermTwo | / Factor TermTwo | EPSILON
        Factor -> ( Expr ) | num | name
        """
        goal = NonTerminal("Goal")
        expr = NonTerminal("Expr")
        expr_two = NonTerminal("ExprTwo")
        term = NonTerminal("Term")
        term_two = NonTerminal("TermTwo")
        factor = NonTerminal("Factor")
        epsilon = Epsilon()
        name = Terminal(CHARACTER, "name")
        num = Terminal(CHARACTER, "num")
        plus = Terminal(CHARACTER, "+")
        minus = Terminal(CHARACTER, "-")
        div = Terminal(CHARACTER, "/")
        asteroid = Terminal(CHARACTER, "*")
        open_parenthesis = Terminal(CHARACTER, "(")
        close_parenthesis = Terminal(CHARACTER, ")")
        eof = EOF()

        production = Productions(
            {
                goal: [[expr]],
                expr: [[term, expr_two]],
                expr_two: [[plus, term, expr_two], [minus, term, expr_two], [epsilon]],
                term: [[factor, term_two]],
                term_two: [
                    [asteroid, factor, term_two],
                    [div, factor, term_two],
                    [epsilon],
                ],
                factor: [[open_parenthesis, expr, close_parenthesis], [num], [name]],
            }
        )

        production.set_start_symbol(goal)

        fs = FirstPlusSet(production)
        fs.compute()

        real_result = fs.first_plus_set

        expect_result = {
            NonTerminal("Goal"): {
                Terminal(CHARACTER, "name"): 0,
                Terminal(CHARACTER, "num"): 0,
                Terminal(CHARACTER, "("): 0,
            },
            NonTerminal("Expr"): {
                Terminal(CHARACTER, "name"): 0,
                Terminal(CHARACTER, "num"): 0,
                Terminal(CHARACTER, "("): 0,
            },
            NonTerminal("ExprTwo"): {
                EOF(): 2,
                Terminal(CHARACTER, "+"): 0,
                Terminal(CHARACTER, "-"): 1,
                Terminal(CHARACTER, ")"): 2,
            },
            NonTerminal("Term"): {
                Terminal(CHARACTER, "name"): 0,
                Terminal(CHARACTER, "num"): 0,
                Terminal(CHARACTER, "("): 0,
            },
            NonTerminal("TermTwo"): {
                EOF(): 2,
                Terminal(CHARACTER, "+"): 2,
                Terminal(CHARACTER, "-"): 2,
                Terminal(CHARACTER, "/"): 1,
                Terminal(CHARACTER, "*"): 0,
                Terminal(CHARACTER, ")"): 2,
            },
            NonTerminal("Factor"): {
                Terminal(CHARACTER, "name"): 2,
                Terminal(CHARACTER, "num"): 1,
                Terminal(CHARACTER, "("): 0,
            },
        }

        self.assertEqual(real_result, expect_result)
