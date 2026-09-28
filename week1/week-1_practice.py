# Week 1 Practice Program
# This program checks whether a number is even or odd
# and whether it is positive, negative, or zero.
def main():
    number = int(input("Enter a number: "))

    # Check whether the number is even or odd
    if number % 2 == 0:
        print("The number is even.")
    else:
        print("The number is odd.")

    # Check whether the number is positive, negative, or zero
    if number > 0:
        print("The number is positive.")
    elif number < 0:
        print("The number is negative.")
    else:
        print("The number is zero.")


if __name__ == "__main__":
    main()