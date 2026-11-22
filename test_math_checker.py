
from src.math_checker import check_equation_step

tests = [
    ("2x + 3 = 11", "2x = 8"),
    ("2x + 3 = 11", "x = 4"),
    ("2x + 3 = 11", "2x = 7"),
    ("2x + 3 = 11", "2x = 11"),
]

for original, new in tests:
    result = check_equation_step(original, new)

    print(f"\nOriginal: {original}")
    print(f"New:      {new}")
    print(f"Valid:    {result['valid']}")
    print(f"Feedback: {result['feedback']}")
