from MicroCompiler.LR.closure_operation import closure_operation
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
    lr_1_item = {
        LR1Item(
            NonTerminal("Goal"), RightHandSide([NonTerminal("SheepNoise")], 0), EOF()
        )
    }

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

    closure_items = closure_operation(lr_1_item, productions, first_set)
    expected_state = State(
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
    assert closure_items == expected_state
