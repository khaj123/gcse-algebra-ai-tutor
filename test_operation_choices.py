
from src.operation_choices import generate_operation_choices

test_equations = [
    "2x + 3 = 11",
    "2x = 8",
    "3x - 5 = 10",
]

for equation in test_equations:
    print(f"\nEquation: {equation}")

    choices = generate_operation_choices(equation)

    for choice in choices:
        print(
            f"  {choice['label']} "
            f"| Recommended: {choice['recommended']}"
        )
