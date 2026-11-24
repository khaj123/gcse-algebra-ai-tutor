from sympy import simplify, sympify
from .math_checker import parse_equation

def apply_operation(equation_text, operation, amount):
    eq=parse_equation(equation_text)
    n=sympify(amount)
    if n.is_number is not True or n.is_finite is not True: raise ValueError('Invalid amount')
    if operation=='Add': f=lambda a:a+n
    elif operation=='Subtract': f=lambda a:a-n
    elif operation=='Multiply' and n!=0: f=lambda a:a*n
    elif operation=='Divide' and n!=0: f=lambda a:a/n
    else: raise ValueError('Invalid operation or zero factor')
    return f'{simplify(f(eq.lhs))} = {simplify(f(eq.rhs))}'
