from MicroCompiler.LR.goto_operation import goto_operation
from MicroCompiler.LR.lr_one_item import LR1Item
from MicroCompiler.LR.rhs import RightHandSide
from MicroCompiler.LR.state import State
from MicroCompiler.Lookahead.EOF import EOF
from MicroCompiler.Lookahead.FirstSet import FirstSet
from MicroCompiler.Lookahead.NonTerminal import NonTerminal
from MicroCompiler.Lookahead.Terminal import Terminal
from MicroCompiler.Productions import Productions


def test_by_sheep_noise_language():
    # Goal -> . SheepNoise , EOF
    s0 = State(
        [
            #  [Goal -> • SheepNoise, EOF]
            LR1Item(
                NonTerminal("Goal"),
                RightHandSide([NonTerminal("SheepNoise")], 0),
                lookahead=EOF(),
            ),
            #  [SheepNoise -> • SheepNoise baa, EOF]
            LR1Item(
                NonTerminal("SheepNoise"),
                RightHandSide([NonTerminal("SheepNoise"), Terminal("sound", "baa")], 0),
                lookahead=EOF(),
            ),
            #  [SheepNoise -> • baa, EOF]
            LR1Item(
                NonTerminal("SheepNoise"),
                RightHandSide([Terminal("sound", "baa")], 0),
                lookahead=EOF(),
            ),
            #  [SheepNoise -> • SheepNoise baa, baa]
            LR1Item(
                NonTerminal("SheepNoise"),
                RightHandSide([NonTerminal("SheepNoise"), Terminal("sound", "baa")], 0),
                lookahead=Terminal("sound", "baa"),
            ),
            #  [SheepNoise -> • baa, baa]
            LR1Item(
                NonTerminal("SheepNoise"),
                RightHandSide([Terminal("sound", "baa")], 0),
                lookahead=Terminal("sound", "baa"),
            ),
        ]
    )

    productions = Productions(
        {
            # Goal -> SheepNoise
            NonTerminal("Goal"): [[NonTerminal("SheepNoise")]],
            # SheepNoise -> SheepNoise baa
            #             | baa
            NonTerminal("SheepNoise"): [
                [NonTerminal("SheepNoise"), Terminal("sound", "baa")],
                [Terminal("sound", "baa")],
            ],
        }
    )

    first_set = FirstSet(productions)
    first_set.compute()

    new_closure_items = goto_operation(
        s0, Terminal("sound", "baa"), productions, first_set
    )

    expected_new_closure_items = State([
        #  [SheepNoise -> baa •, EOF]
        LR1Item(
            NonTerminal("SheepNoise"),
            RightHandSide([Terminal("sound", "baa")], 1),
            lookahead=EOF(),
        ),
        #  [SheepNoise -> baa •, baa]
        LR1Item(
            NonTerminal("SheepNoise"),
            RightHandSide([Terminal("sound", "baa")], 1),
            lookahead=Terminal("sound", "baa"),
        ),
    ])

    assert new_closure_items == expected_new_closure_items
