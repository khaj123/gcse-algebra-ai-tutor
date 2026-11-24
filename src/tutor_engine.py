from .math_checker import diagnose

def student_stage(selected, attempts):
    if selected is None: return 'operation'
    if attempts and not attempts[-1]['valid']: return 'correction'
    return 'arithmetic'

def evaluate_attempt(equation, choice, answer):
    return diagnose(equation,choice['operation'],choice['amount'],answer)
