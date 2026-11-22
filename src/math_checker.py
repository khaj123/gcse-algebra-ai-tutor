
from sympy import Eq, Symbol, simplify, solve, sympify
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

x = Symbol("x")

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
)


def parse_equation(equation_text):
    """Convert an equation string into a SymPy equation."""

    if equation_text.count("=") != 1:
        raise ValueError(
            "Please enter an equation containing one equals sign."
        )

    left_text, right_text = equation_text.split("=")

    if not left_text.strip() or not right_text.strip():
        raise ValueError("Both sides of the equation are required.")

    left = parse_expr(
        left_text.strip(),
        local_dict={"x": x},
        transformations=TRANSFORMATIONS,
    )

    right = parse_expr(
        right_text.strip(),
        local_dict={"x": x},
        transformations=TRANSFORMATIONS,
    )

    if left.free_symbols.union(right.free_symbols) - {x}:
        raise ValueError("Only equations involving x are supported.")

    return Eq(left, right, evaluate=False)


def check_equation_step(original_text, new_text):
    """
    Check whether two equations have the same solution set.

    This is a preliminary equivalence check, not yet a
    verification of the student's claimed operation.
    """

    try:
        original = parse_equation(original_text)
        new = parse_equation(new_text)

        original_solutions = set(solve(original, x))
        new_solutions = set(solve(new, x))

        if original_solutions == new_solutions:
            return {
                "valid": True,
                "feedback": (
                    "Both equations have the same solution set."
                ),
            }

        return {
            "valid": False,
            "feedback": (
                "These equations do not have the same solutions. "
                "Check whether you applied the operation correctly."
            ),
        }

    except Exception as error:
        return {
            "valid": False,
            "feedback": f"Could not check this step: {error}",
        }
