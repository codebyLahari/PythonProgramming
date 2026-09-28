'''
This program asks for a student's name and five test scores.
The scores are stored in a list. A loop is used to collect
and display the scores. The program calculates the average
and uses decisions to determine the student's letter grade.
'''

def main():
    print("Student Score Analyzer")
    print("----------------------")

    # String
    student_name = input("Enter student name: ")

    # Empty list for storing scores
    scores = []

    # Loop to get 5 scores
    for i in range(5):
        score = float(input("Enter score " + str(i + 1) + ": "))
        scores.append(score)

    # Calculate average
    total = 0

    for score in scores:
        total = total + score

    average = total / len(scores)

    # Decision statements
    if average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 60:
        grade = "D"
    else:
        grade = "F"

    # Display results
    print()
    print("Student:", student_name)
    print("Scores:")

    for score in scores:
        print(score)

    print("Average:", round(average, 2))
    print("Grade:", grade)


if __name__ == "__main__":
    main()
