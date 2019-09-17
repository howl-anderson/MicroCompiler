from demo.arithmetic_calculator.arithmetic_calculator import \
    arithmetic_calculator
from demo.arithmetic_calculator.test_cases import test_cases
from demo.arithmetic_calculator.user_level_parser import Parser

user_level_parser = Parser()

for index, (token_list, expected_result) in enumerate(test_cases):
    print("working on: ", token_list)
    result = arithmetic_calculator("output.yaml", token_list, user_level_parser)
    if result != expected_result:
        print("test failed: at #", index)
        print(token_list, result)
        break
