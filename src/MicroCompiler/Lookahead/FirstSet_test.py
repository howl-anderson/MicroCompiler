import unittest
import pprint

from MicroCompiler.Productions import Productions
from .Epsilon import Epsilon
from .EOF import EOF
from .FirstSet import FirstSet
from .NonTerminal import NonTerminal
from .Terminal import CHARACTER
from .Terminal import Terminal
from .SymbolSet import SymbolSet


class TestFirstSet(unittest.TestCase):
    def test_conception(self):
        statement = NonTerminal("Statement")
        expression = NonTerminal("Expression")
        semicolon = Terminal(CHARACTER, ";")
        plus = Terminal(CHARACTER, "+")
        minus = Terminal(CHARACTER, "-")

        production = Productions({
            statement: [
                [expression, semicolon]
            ],
            expression: [
                [plus],
                [minus]
            ]
        })

        production.set_start_symbol(statement)

        fs = FirstSet(production)
        fs.compute()
        print(fs.first_set)

    def test_epsilon(self):
        statement = NonTerminal("Statement")
        expression = NonTerminal("Expression")
        epsilon = Epsilon()
        semicolon = Terminal(CHARACTER, ";")
        plus = Terminal(CHARACTER, "+")
        minus = Terminal(CHARACTER, "-")

        production = Productions({
            statement: [
                [expression, semicolon],
            ],
            expression: [
                [plus],
                [minus],
                [epsilon]
            ]
        })

        production.set_start_symbol(statement)

        fs = FirstSet(production)
        fs.compute()
        print(fs.first_set)

        print(fs.first_set_table)
        print(fs.first_set_mapping)

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

        production = Productions({
            goal: [
                [expr],
            ],
            expr: [
                [term, term_two]
            ],
            expr_two: [
                [plus, term, expr_two],
                [minus, term, expr_two],
                [epsilon]
            ],
            term: [
                [factor, term_two]
            ],
            term_two: [
                [asteroid, factor, term_two],
                [div, factor, term_two],
                [epsilon]
            ],
            factor: [
                [open_parenthesis, expr, close_parenthesis],
                [num],
                [name]
            ]
        })

        production.set_start_symbol(goal)

        fs = FirstSet(production)
        fs.compute()
        real_result = fs.first_set

        expect_result = {
            eof: SymbolSet({eof}),
            plus: SymbolSet({plus}),
            minus: SymbolSet({minus}),
            epsilon: SymbolSet({epsilon}),
            asteroid: SymbolSet({asteroid}),
            div: SymbolSet({div}),
            open_parenthesis: SymbolSet({open_parenthesis}),
            close_parenthesis: SymbolSet({close_parenthesis}),
            num: SymbolSet({num}),
            name: SymbolSet({name}),
            expr_two: SymbolSet({plus, minus, epsilon}),
            term_two: SymbolSet({asteroid, div, epsilon}),
            factor: SymbolSet({open_parenthesis, num, name}),
            term: SymbolSet({open_parenthesis, num, name}),
            expr: SymbolSet({open_parenthesis, num, name}),
            goal: SymbolSet({open_parenthesis, num, name})
        }

        # pprint.pprint(real_result)

        self.maxDiff = None
        self.assertEqual(real_result, expect_result)
