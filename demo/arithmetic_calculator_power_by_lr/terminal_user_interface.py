from demo.arithmetic_calculator_power_by_lr.arithmetic_calculator import ArithmeticCalculator

ac = ArithmeticCalculator()

# Continue while true.
while True:
    # Get input.
    print("> ", end="")
    value = input()

    # Break if user types q.
    if value == "q":
        break

    # echo value.
    print("You typed: ", value)

    result = ac.eval(value)

    # print result
    print("Result: ", result)

# Exit message.
print("You quit.")
