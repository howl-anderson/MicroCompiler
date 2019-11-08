from MicroCompiler.demo.arithmetic_calculator.lr.arithmetic_calculator import (
    ArithmeticCalculator,
)


def test_arithmetic_calculator():
    test_cases = (
        ("6+2", 8),
        ("6+2+2", 10),
        ("6-2", 4),
        ("6-2-2", 2),
        ("6/2", 3.0),
        ("12/6/2", 1),
        ("6*2", 12),
        ("3*6*2", 36),
        ("6+2/2", 7),
        ("6/2+2", 5),
        ("6+2*2", 10),
        ("6*2+2", 14),
        ("6*(2+2)", 24),
        ("(2+2)*6", 24),
        ("(2+2+2)*6", 36),
        ("(2+2/2)*6", 18),
        ("(2+2/2)*6/(2+2*2)", 3),
    )

    ac = ArithmeticCalculator()

    for token_list, expected_result in test_cases:
        print("working on: ", token_list)
        result = ac.eval(token_list)
        if result != expected_result:
            print("test failed: at {}", (token_list, expected_result))
            break

    print("success!")
