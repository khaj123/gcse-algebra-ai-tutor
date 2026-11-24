from .math_checker import validate_equation, x

def hint_text(stage,level,choice=None,diagnosis=None,equation=None):
    e=validate_equation(equation); a=e.lhs.diff(x); b=e.lhs.subs(x,0)
    if stage=='operation':
        return (['Look at the number beside the x term. Which remaining choice would help remove it?' ,f'What would undo the constant {b}?','Imagine making the orange term zero. Which remaining choice would do that?' ] if b else ['What number is multiplying x?',f'How could you undo multiplication by {a}?','Imagine splitting the x terms into groups until only one x remains.'])[level-1]
    side='both sides'
    if diagnosis:
        if diagnosis['left_correct']: side='the right side'
        elif diagnosis['right_correct']: side='the left side'
    op=choice['operation']; n=choice['amount']; target=e.rhs if side=='the right side' else e.lhs
    sign={'Add':'+','Subtract':'−','Multiply':'×','Divide':'÷'}[op]
    return [f'Focus on {side}. What does {choice["label"].lower()} mean here?',f'Work out ({target}) {sign} {n} separately, then check the other side.', 'Use the visual below to work through the operation, then write your new equation.'][level-1]
