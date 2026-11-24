import html
from sympy import Symbol, simplify, latex
from .math_checker import parse_equation


def equation_tex(text):
    eq = parse_equation(text)
    return latex(eq.lhs) + '=' + latex(eq.rhs)


def transformation_tex(text, op, n):
    eq = parse_equation(text)
    a, b, n = latex(eq.lhs), latex(eq.rhs), latex(n)
    if op == 'Add': return rf'({a})+{n}=({b})+{n}'
    if op == 'Subtract': return rf'({a})-{n}=({b})-{n}'
    if op == 'Multiply': return rf'{n}({a})={n}({b})'
    return rf'\frac{{{a}}}{{{n}}}=\frac{{{b}}}{{{n}}}'


def _tile(value, background, foreground):
    return (f'<span style="display:inline-block;padding:12px 18px;border-radius:14px;'
            f'background:{background};color:{foreground};font-size:clamp(20px,3vw,32px);'
            f'font-weight:750;line-height:1.3">{html.escape(str(value))}</span>')


def equation_tiles(text, latest=False):
    eq = parse_equation(text)
    x = Symbol('x')
    a = simplify(eq.lhs.diff(x))
    b = simplify(eq.lhs.subs(x, 0))
    if simplify(eq.lhs - a*x - b) != 0:
        return f'<div style="text-align:center">{html.escape(str(text))}</div>'
    variable = ('x' if a == 1 else '−x' if a == -1 else f'{a}x')
    left = _tile(variable, '#dbeafe', '#1d4ed8')
    if b != 0:
        sign = '+' if b > 0 else '−'
        left += f'<span style="font-size:27px;font-weight:700;color:#334155">{sign}</span>'
        left += _tile(abs(b), '#ffedd5', '#9a3412')
    border = '3px solid #8b5cf6' if latest else '1px solid #dbe3f2'
    return (f'<div style="display:flex;justify-content:center;align-items:center;gap:12px;'
            f'flex-wrap:wrap;padding:24px 12px;border-radius:20px;background:white;'
            f'border:{border};box-shadow:0 5px 18px #1e293b0b">'
            f'{left}<span style="font-size:30px;font-weight:800;color:#334155">=</span>'
            f'{_tile(eq.rhs, "#d1fae5", "#065f46")}</div>')


def balance_visual(text, op, amount, diagnosis=None):
    eq = parse_equation(text)
    left_bad = diagnosis is not None and not diagnosis.get('left_correct', False)
    right_bad = diagnosis is not None and not diagnosis.get('right_correct', False)
    def panel(title, expression, bad):
        border = '#f59e0b' if bad else '#93c5fd'
        label = 'Check this side' if bad else 'Apply the same operation'
        return (f'<div style="flex:1;min-width:220px;padding:18px;border:2px solid {border};'
                f'border-radius:16px;background:#fff">'
                f'<div style="font-size:13px;font-weight:700;color:#475569">{title}</div>'
                f'<div style="font-size:21px;color:#1e293b;margin:12px 0;overflow-wrap:anywhere">'
                f'{html.escape(expression)}</div><div style="font-size:13px;color:#64748b">{label}</div></div>')
    op_label = {'Add': '+', 'Subtract': '−', 'Multiply': '×', 'Divide': '÷'}.get(op, op)
    def expression(v):
        return f'({v}) {op_label} {amount}'
    return (f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin:14px 0">'
            f'{panel("LEFT SIDE", expression(eq.lhs), left_bad)}'
            f'{panel("RIGHT SIDE", expression(eq.rhs), right_bad)}</div>')


def arithmetic_number_line(start, operation, amount):
    """A number line with an unknown endpoint: never reveals the answer."""
    try:
        start = int(start)
        amount = int(amount)
    except (ValueError, TypeError):
        return ''
    if operation not in ('Add', 'Subtract') or amount <= 0 or amount > 12:
        return ''
    # Display start and direction only; students calculate the destination.
    direction = 'left' if operation == 'Subtract' else 'right'
    arrows = '← ' if direction == 'left' else ' →'
    dots = ' '.join(['●'] * min(amount, 8))
    return (f'<div style="padding:18px;border-radius:16px;background:#f0f9ff;'
            f'border:1px solid #bae6fd;text-align:center">'
            f'<div style="font-weight:700;color:#075985">Start at {start}</div>'
            f'<div style="font-size:22px;letter-spacing:5px;color:#0284c7;margin:8px 0">'
            f'{arrows if direction == "left" else ""}{dots}{arrows if direction == "right" else ""}</div>'
            f'<div style="color:#334155">Count {amount} steps {direction}. Where do you land?</div></div>')


def operation_clue(text):
    e=parse_equation(text); x=Symbol('x'); b=e.lhs.subs(x,0)
    return equation_tiles(text,latest=True)+('<p>Focus on the orange term. How could you make it zero?</p>' if b else '<p>Focus on the blue term. How could you get just one x?</p>')


def worked_frames(text,op,n,new):
    e=parse_equation(text); x=Symbol('x'); a=e.lhs.diff(x); b=e.lhs.subs(x,0)
    esc=lambda v:html.escape(str(v).replace('*','').replace('-','−'))
    def ink(v,c='#334155',cross=False):
        return f'<span style="color:{c};position:relative;display:inline-block;'+('text-decoration:line-through;text-decoration-color:#be123c;text-decoration-thickness:3px;' if cross else '')+'">'+esc(v)+'</span>'
    blue='#1d4ed8'; orange='#9a3412'; green='#047857'; red='#be123c'
    def board(*rows):
        return '<div style="background:#fff;color:#334155;border:1px solid #cbd5e1;border-radius:14px;padding:20px;font-family:Georgia,serif;font-style:italic;font-size:clamp(20px,3vw,29px);text-align:center;line-height:2.4;background-image:repeating-linear-gradient(white 0px,white 39px,#e2e8f0 40px)">'+ '<br>'.join(rows)+'</div>'
    var=ink('x' if a==1 else '-x' if a==-1 else str(a)+'x',blue)
    const=(' '+ink(('+' if b>0 else '-')+str(abs(b)),orange)) if b else ''
    original=var+const+' = '+ink(e.rhs,green)
    if op in ('Add','Subtract'):
        delta=n if op=='Add' else -n
        change=('+' if delta>=0 else '-')+str(abs(delta))
        line=var+const+' '+ink(change,red)+' = '+ink(e.rhs,green)+' '+ink(change,red)
        if b+delta==0 and b:
            cancelled=var+' '+ink(('+' if b>0 else '-')+str(abs(b)),orange,True)+' '+ink(change,red,True)+' = '+ink(e.rhs,green)+' '+ink(change,red)
            explanation=f'{b} and {delta} add up to zero, so those terms cancel. On the right, calculate {e.rhs} {change}.'
        else:
            cancelled=line;explanation=f'Combine the constant terms on the left and calculate {e.rhs} {change} on the right.'
        return [('Look at the starting equation',board(original),'We want to get x on its own.'),('Apply the same operation',board(original,line),f'{op} {n} on both sides to keep the equation balanced.'),('Simplify each side',board(original,cancelled),explanation),('The next equation',board(original,cancelled)+equation_tiles(new,True),f'The right side becomes {e.rhs+delta}. This gives the next equation.')]
    if op=='Divide':
        def frac(top):return '<span style="display:inline-flex;flex-direction:column;vertical-align:middle;line-height:1.3"><span style="border-bottom:2px solid #334155">'+top+'</span>'+ink(n,red)+'</span>'
        line=frac(var+const)+' = '+frac(ink(e.rhs,green))
        detail=ink(f'{a} ÷ {n} = {a/n}',blue)+' &nbsp; | &nbsp; '+ink(f'{e.rhs} ÷ {n} = {e.rhs/n}',green)
        return [('Look at the starting equation',board(original),'The number multiplying x tells us how many x terms there are.'),('Divide both sides',board(original,line),f'Divide both sides by {n} to undo multiplication.'),('Work out each division',board(line,detail),'Divide the coefficient of x and the number on the right by the same amount.'),('The next equation',board(line)+equation_tiles(new,True),'Now simplify both sides. The new equation stays balanced.')]
    return [('Starting equation',board(original),'Keep both sides balanced.'),('Apply the operation',board(ink(f'{n} × ({e.lhs})')+' = '+ink(f'{n} × ({e.rhs})')),f'Multiply both sides by {n}.'),('The next equation',equation_tiles(new,True),'Simplify both sides.')]
