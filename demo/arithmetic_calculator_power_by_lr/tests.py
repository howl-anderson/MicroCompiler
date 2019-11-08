from demo.arithmetic_calculator_power_by_lr.arithmetic_calculator import ArithmeticCalculator
from demo.arithmetic_calculator_power_by_lr.test_cases import test_cases

ac = ArithmeticCalculator()

for token_list, expected_result in test_cases:
    print("working on: ", token_list)
    result = ac.eval(token_list)
    if result != expected_result:
        print("test failed: at {}", (token_list, expected_result))
        break

print("success!")
