from demo.arithmetic_calculator.main_with_lexer import main

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

    result = main(value)

    # print result
    print("Result: ", result)

# Exit message.
print("You quit.")
