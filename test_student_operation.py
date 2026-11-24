
from src.math_checker import check_student_operation

tests = [
    ("2x + 3 = 11", "Subtract", 3, "2x = 8"),
    ("2x + 3 = 11", "Subtract", 3, "2x = 7"),
    ("2x + 3 = 11", "Subtract", 3, "2x + 3 = 8"),
    ("2x + 3 = 11", "Add", 3, "2x + 6 = 14"),
]

for original, operation, amount, student_answer in tests:
    result = check_student_operation(
        original, operation, amount, student_answer
    )

    print(f"\nStudent answer: {student_answer}")
    print(f"Valid: {result['valid']}")
    print(f"Feedback: {result['feedback']}")
