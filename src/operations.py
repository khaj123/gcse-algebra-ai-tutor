
from sympy import Add, Mul, Pow, S
from src.math_checker import parse_equation


def apply_operation(equation_text, operation, amount):
    """
    Apply the same operation to both sides of an equation.

    Returns a new equation string.
    """
    equation = parse_equation(equation_text)

    left = equation.lhs
    right = equation.rhs
    amount = S(amount)

    if not amount.is_number or amount.is_finite is not True:
        raise ValueError("Enter a finite number.")

    if operation == "Add":
        new_left = left + amount
        new_right = right + amount

    elif operation == "Subtract":
        new_left = left - amount
        new_right = right - amount

    elif operation == "Multiply":
        if amount == 0:
            raise ValueError(
                "Multiplying by zero can lose information."
            )
        new_left = left * amount
        new_right = right * amount

    elif operation == "Divide":
        if amount == 0:
            raise ValueError("You cannot divide by zero.")
        new_left = left / amount
        new_right = right / amount

    else:
        raise ValueError("Unknown operation.")

    from sympy import simplify

    new_left = simplify(new_left)
    new_right = simplify(new_right)

    return f"{new_left} = {new_right}"
