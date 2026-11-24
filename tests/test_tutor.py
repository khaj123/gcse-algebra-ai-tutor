import pytest
from src.math_checker import parse_equation,validate_equation,diagnose
from src.operation_choices import generate_operation_choices
from src.operations import apply_operation
from src.hint_engine import hint_text

def test_safe_parser():
    assert str(parse_equation('2x + 3 = 11').lhs)=='2*x + 3'
    with pytest.raises(ValueError): parse_equation('__import__("os").system("echo hi") = 1')
    with pytest.raises(ValueError): parse_equation('x**100 = 1')

def test_choices():
    choices=generate_operation_choices('2x + 3 = 11')
    assert len(choices)==5
    assert sum(c['recommended'] for c in choices)==1
    assert sum(c['eliminate_on_hint'] for c in choices)==2

def test_diagnosis():
    d=diagnose('2x + 3 = 11','Subtract',3,'2x = 7')
    assert not d['valid'] and d['left_correct'] and not d['right_correct']
    assert diagnose('2x + 3 = 11','Subtract',3,'2x = 8')['valid']

def test_progress():
    assert apply_operation('2x + 3 = 11','Subtract',3)=='2*x = 8'
    assert apply_operation('2x = 8','Divide',2)=='x = 4'

def test_hint_relevance():
    h = hint_text(
        'correction', 1,
        {'label': 'Subtract 3', 'operation': 'Subtract', 'amount': 3},
        {'left_correct': True, 'right_correct': False},
        '2x + 3 = 11'
    )
    assert 'right side' in h.lower() or 'right-hand side' in h.lower()
