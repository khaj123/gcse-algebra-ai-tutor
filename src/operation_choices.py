from sympy import Symbol, simplify
from .math_checker import validate_equation
x=Symbol('x')

def generate_operation_choices(text):
    eq=validate_equation(text)
    a=simplify(eq.lhs.diff(x)); b=simplify(eq.lhs.subs(x,0))
    if b!=0: op,n=('Subtract',b) if b>0 else ('Add',-b)
    elif a!=1: op,n='Divide',a
    else: return []
    options=[(op,n),('Add',5),('Multiply',2),('Divide',3),('Subtract',2),('Add',3),('Divide',2),('Subtract',3),('Multiply',3)]
    result=[]; seen=set()
    for name,amount in options:
        key=(name,str(amount))
        if key in seen: continue
        seen.add(key)
        result.append({'label':f'{name} {amount}','operation':name,'amount':amount,'recommended':name==op and amount==n,'eliminate_on_hint':False})
        if len(result)==5: break
    for c in result[-2:]: c['eliminate_on_hint']=True
    return result
