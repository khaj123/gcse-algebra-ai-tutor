import ast
from sympy import Eq, Symbol, Integer, Rational, simplify
x = Symbol('x')

def _eval(node):
    if isinstance(node, ast.Expression): return _eval(node.body)
    if isinstance(node, ast.Name) and node.id == 'x': return x
    if isinstance(node, ast.Constant) and type(node.value) is int and abs(node.value) <= 1000000: return Integer(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        v = _eval(node.operand); return v if isinstance(node.op, ast.UAdd) else -v
    if isinstance(node, ast.BinOp):
        a,b = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Add): return a+b
        if isinstance(node.op, ast.Sub): return a-b
        if isinstance(node.op, ast.Mult): return a*b
        if isinstance(node.op, ast.Div):
            if b == 0: raise ValueError('Cannot divide by zero')
            return a/b
    raise ValueError('Use numbers, x, +, -, *, / and parentheses only.')

def _side(s):
    import re
    s = re.sub(r'(?<=\d)\s*(?=x)', '*', s.strip())
    if len(s)>100: raise ValueError('Equation is too long')
    return _eval(ast.parse(s,mode='eval'))

def parse_equation(text):
    if text.count('=')!=1: raise ValueError('Enter exactly one equals sign.')
    a,b=text.split('='); return Eq(_side(a),_side(b),evaluate=False)

def validate_equation(text):
    e=parse_equation(text)
    if e.rhs.has(x): raise ValueError('Put x on the left-hand side.')
    a=simplify(e.lhs.diff(x)); b=simplify(e.lhs.subs(x,0))
    if a==0 or a.has(x) or simplify(e.lhs-a*x-b)!=0 or e.rhs.has(x):
        raise ValueError('Use a linear equation of the form ax + b = c.')
    if any(v.is_number is not True or v.is_finite is not True for v in (a,b,e.rhs)):
        raise ValueError('Only finite numerical coefficients are supported.')
    return e

def diagnose(original,operation,amount,student):
    from .operations import apply_operation
    try:
        expected=parse_equation(apply_operation(original,operation,amount))
        actual=parse_equation(student)
        left=simplify(expected.lhs-actual.lhs)==0
        right=simplify(expected.rhs-actual.rhs)==0
        return {'valid':left and right,'left_correct':left,'right_correct':right,
                'feedback':('Both sides are correct!' if left and right else
                  'The left side looks right. Check your arithmetic on the right.' if left else
                  'The right side looks right. Check your arithmetic on the left.' if right else
                  'Check both sides: apply the operation equally and simplify.')}
    except Exception as exc:
        return {'valid':False,'left_correct':False,'right_correct':False,'feedback':str(exc)}

def check_student_operation(original,operation,amount,student):
    return diagnose(original,operation,amount,student)


def check_equation_step(original_text, new_text):
    """Legacy compatibility: check that two equations have identical solutions."""
    from sympy import solve
    try:
        original = parse_equation(original_text)
        new = parse_equation(new_text)
        original_solutions = set(solve(original, x))
        new_solutions = set(solve(new, x))
        if original_solutions == new_solutions:
            return {
                'valid': True,
                'feedback': 'Both equations have the same solution set.',
            }
        return {
            'valid': False,
            'feedback': 'These equations do not have the same solutions. Check your algebra.',
        }
    except Exception as error:
        return {'valid': False, 'feedback': f'Could not check this step: {error}'}
