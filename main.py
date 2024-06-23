# exercise 1
def excersie_1() -> None:
    """
    excersie_1 will input a five-digit number.
    Then the function will print the number, each of its digits and the sum of its digits.
    :return: None
    """

    # input a number and print it
    num: int = (int(input("Input a five digit number: ")))
    print(num)

    # print each digit and get sum
    digit: int
    sum_digits: int = 0

    while num > 0:
        digit = num % 10
        print(digit)
        sum_digits += digit
        num //= 10

    print(sum_digits)


# exercise 2
def excersie_2() -> None:
    """
    excersie_2 will input a five-digit number.
    Then the function will print the number, each of its digits and the sum of its digits.
    This time we will also implement input validation.
    :return: None
    """

    # input a number and print it using input validation
    num: int = 0
    while num < 10000 or num > 99999:
        num: int = (int(input("Input a five digit number: ")))

    print(num)

    # print each digit and get sum
    digit: int
    sum_digits: int = 0

    while num > 0:
        digit = num % 10
        print(digit)
        sum_digits += digit
        num //= 10

    print(sum_digits)


# exercise 3
def excersie_3() -> None:
    """
    excersie_3 will input a string and will output the encryption of the string using the "b-language" encryption.
    :return: None
    """

    # define vowel list
    vowels: list[str] = ["a", "e", "i", "o", "u"]

    # input a string and prepare for encryption
    string: str = input("Input a string: ")
    result: str = ""

    for char in string:
        result += char

        if char in vowels:
            result += "b"
            result += char

    print(result)


# exercise 4
def excersie_4(exercises_file: str, solutions_file: str) -> None:
    """
    exercise_4 will read the exercises on the exercises file and write the solutions on the solutions file.
    :param exercises_file: the name of the file containing the exercises
    :param solutions_file: the name of the file were the solutions will be written to
    :return: None
    """

    # attempt to read the exercises file
    try:
        with open(exercises_file, "r") as exercises_file:
            exercises = exercises_file.readlines()

        solutions: list[str] = []

        # read each exercise
        for exercise in exercises:
            # strip all whitespace characters
            exercise = exercise.strip()
            # split exercise
            sections = exercise.split()
            if len(sections) != 3:
                continue

            # extract the numbers
            num1: int = int(sections[0])
            operation: chr = sections[1]
            num2: int = int(sections[2])

            # calculate the solution base on operation
            result: int
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                result = num1 / num2
            else:
                continue

            # format solution as required
            solution: str = f"{exercise} = {result}"
            solutions.append(solution)

        # write the solutions to the solutions file
        with open(solutions_file, "w") as solutions_file:
            for solution in solutions:
                solutions_file.write(f"{solution}\n")

    # catch exceptions for the file opening
    except FileNotFoundError:
        print(f"Error: THe file {exercises_file} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the exercises file: {e}")


# main function for testing
def main() -> None:
    """
    main() will start the main function to test the functions for all exercises.
    :return: None
    """

    excersie_1()
    excersie_2()
    excersie_3()
    excersie_4("homework.txt", "solutions.txt")


if __name__ == "__main__":
    main()
