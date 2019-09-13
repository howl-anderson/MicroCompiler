import unittest
import pprint

from MicroCompiler.Productions import Productions
from MicroCompiler.Lookahead.Epsilon import Epsilon
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.FirstSet import FirstSet
from MicroCompiler.Lookahead.FollowSet import FollowSet
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import CHARACTER
from MicroCompiler.Lookahead.Terminal import Terminal


class TestFollowSet(unittest.TestCase):
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

        fs = FirstSet(production)
        fs.compute()
        first_set = fs.first_set

        fs = FollowSet(production, first_set)
        fs.compute()
        print(fs.follow_set)

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

        fs = FirstSet(production)
        fs.compute()
        first_set = fs.first_set

        fs = FollowSet(production, first_set)
        fs.compute()
        print(fs.follow_set)

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

        fs = FirstSet(production)
        fs.compute()
        first_set = fs.first_set

        fs = FollowSet(production, first_set)
        fs.compute()
        real_result = fs.follow_set

        expect_result = {
            NonTerminal("Goal"): {EOF()},
            NonTerminal("Expr"): {Terminal(CHARACTER, ")"), EOF()},
            NonTerminal("ExprTwo"): {Terminal(CHARACTER, ")"), EOF()},
            NonTerminal("Term"): {
                EOF(),
                Terminal(CHARACTER, "+"),
                Terminal(CHARACTER, "-"),
                Terminal(CHARACTER, ")"),
            },
            NonTerminal("TermTwo"): {
                EOF(),
                Terminal(CHARACTER, "+"),
                Terminal(CHARACTER, "-"),
                Terminal(CHARACTER, ")"),
            },
            NonTerminal("Factor"): {
                EOF(),
                Terminal(CHARACTER, "+"),
                Terminal(CHARACTER, "-"),
                Terminal(CHARACTER, "/"),
                Terminal(CHARACTER, "*"),
                Terminal(CHARACTER, ")"),
            },
        }

        self.assertEqual(real_result, expect_result)
