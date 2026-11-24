from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from sympy import simplify
from src.math_checker import validate_equation, x
from src.operation_choices import generate_operation_choices
from src.operations import apply_operation
from src.tutor_engine import evaluate_attempt
from src.hint_engine import hint_text
from src.llm_tutor import personalised_hint, extract_questions
from src.visualisations import equation_tiles, equation_tex, transformation_tex, balance_visual, worked_frames, operation_clue
import html, random, re, os

def simple_question(text):
    # Only accept a complete, unambiguous simple equation, never a substring.
    m = re.fullmatch(r"\s*(?:solve\s+(?:the equation\s+)?|find\s+x\s*[: ]\s*)?([+-]?(?:\d+\s*\*?\s*)?x(?:\s*[+-]\s*\d+)?\s*=\s*[+-]?\d+)\s*[.?]?\s*", clean(text), re.IGNORECASE)
    return m.group(1).lower() if m else None


st.set_page_config(page_title='AlgebraStep',layout='wide')
st.markdown('''<style>
.block-container{max-width:1150px;padding-top:2rem}
h1,h2,h3{letter-spacing:-.025em}
.stButton button{border-radius:10px;min-height:44px;font-weight:600;transition:background .15s}
.stButton button[kind="primary"]{background:#2458C6;color:white;border-color:#2458C6}
.stButton button[kind="secondary"]{background:#dbeafe;color:#1e40af;border-color:#93b4e8}
.stButton button[kind="secondary"]:hover{background:#bfdbfe;color:#1e3a8a}
[class*="st-key-op_"] button{width:100%;min-height:52px}
[class*="st-key-op_"] button:disabled{color:#475569!important;opacity:1}
[class*="st-key-eliminated_"] button:disabled{color:#475569!important;opacity:1}
[class*="st-key-eliminated_"] button p{text-decoration:line-through!important}
[class*="st-key-eliminated_"] button:disabled{color:#334155!important;background:#e5e7eb!important}
[class*="st-key-op_"] button[kind="secondary"]{background:#dbeafe!important;color:#1e40af!important}
[class*="st-key-eliminated_"] button{width:100%;min-height:52px}
.stButton button:focus-visible{outline:3px solid #1d4ed8;outline-offset:3px}
.stButton button:disabled{background:#e5e7eb!important;color:#64748b!important;border-color:#e5e7eb!important}
.st-key-hint_action button:not(:disabled){background:#7c3aed;color:white;border-color:#7c3aed}
.st-key-stuck_action button:not(:disabled){background:#fff1db;color:#92400e;border-color:#d97706}
.st-key-continue_action button:not(:disabled){background:#15803d;color:white;border-color:#15803d}
.st-key-replay_action button{background:#f3e8ff!important;color:#6b21a8!important;border-color:#c4b5fd!important}
.hero{background:#eff6ff;border:1px solid #bfdbfe;border-radius:18px;padding:24px;margin:8px 0 20px;color:#1e3a8a}
.hero h2{color:#1e3a8a;margin:0 0 8px;padding:0;font-size:1.8rem}.hero p{color:#334155;margin:0;font-size:1.05rem}
</style>''',unsafe_allow_html=True)
s=st.session_state
for k,v in dict(page='home',questions=[],completed=[],steps=[],operations=[],revealed=[],nonce=0,op_hints=[],removed=[],op_history=[],frame=0,selected=None,hints=[],attempts=[],confirm=False,reveal=False).items():
    if k not in s:s[k]=v

def reset():
    s.selected=None;s.op_hints=[];s.removed=[];s.op_history=[];s.frame=0;s.hints=[];s.attempts=[];s.confirm=False;s.reveal=False;s.nonce+=1

def clean(text):return text.strip().replace('−','-').replace('×','*').replace('÷','/')
def start(text):
    validate_equation(text);s.steps=[text];s.operations=[];s.revealed=[];reset();s.page='solve'

def advance(text,label,revealed=False):
    s.steps.append(text);s.operations.append(label);s.revealed.append(revealed);reset();st.rerun()

st.title('AlgebraStep')
st.caption('Your GCSE linear equation tutor')
if s.page!='home':
    if st.button('Home',key='home_nav',icon=':material/home:'):
        s.resume_page=s.page;s.page='home';st.rerun()
if s.page=='home':
    if s.get('resume_page') and st.button('Resume previous session',key='resume_nav'):
        s.page=s.resume_page;s.resume_page=None;st.rerun()
    st.markdown('<div class="hero"><h2>Build your confidence in algebra.</h2><p>Practise GCSE linear equations at your own pace. Choose each step yourself, get personalised hints and explore visual explanations when you need help.</p></div>',unsafe_allow_html=True)
    st.subheader('What you can practise')
    a,b=st.columns(2)
    with a:
        with st.container(border=True):
            st.markdown('**One-step equations**');st.latex('x+5=12');st.caption('Get x on its own using one operation.')
    with b:
        with st.container(border=True):
            st.markdown('**Two-step equations**');st.latex('2x+3=11');st.caption('Use two operations to find x.')
    st.caption('Currently supports simple equations using x on one side only. Quadratics, simultaneous equations and graphs are not covered.')
    st.divider()
    st.subheader('What questions do you want to practise?')
    mode=st.radio('Choose how to enter your questions', ['Type or paste','Upload a photo'],horizontal=True)
    text='';photo=None
    if mode=='Type or paste':text=st.text_area('Enter your linear equation problem or paste in several problems you’re struggling with.',placeholder='a) 2x + 3 = 11\nb) 3x - 5 = 16')
    else:
        f=st.file_uploader('Upload a photo of the linear equation questions you need help with.',type=['png','jpg','jpeg'])
        st.caption('Only upload cropped maths questions. Do not include names, faces or school details. The image is sent to Gemini for reading.')
        if f and f.size<=5_000_000:photo=(f.getvalue(),f.type)
        elif f:st.warning('Choose an image smaller than 5 MB.')
    st.caption('AI hints and photo recognition can make mistakes. Question content may be sent to Google Gemini. Please avoid personal information.')
    if st.button('Read questions' if photo else 'Start learning',type='primary',disabled=not(text.strip() or photo)):
        try:
            direct = simple_question(text) if not photo else None
            if direct:
                validate_equation(direct)
                qs=[dict(label='1',text=text,equation=direct,uncertain=False)]
            else:
                with st.spinner('Reading your questions...'):
                    qs=extract_questions(text,photo)
            if not qs:
                st.warning('No equations were found. Check the question or upload a clearer photo.')
            else:
                s.questions=qs;s.completed=[];s.nonce+=1;s.resume_page=None;s.steps=[]
                if direct:
                    s.active=0;start(direct)
                else:
                    s.page='review'
                st.rerun()
        except Exception as exc:
            status=getattr(exc,'code',None)
            if not os.getenv('GEMINI_API_KEY') and not direct:
                st.error('AI reading is not configured. You can still type a simple equation, such as x + 6 = 13.')
            elif status==429:
                st.error('AI reading has reached its usage limit. Try again later or enter one simple equation.')
            elif status in (401,403):
                st.error('AI reading could not authenticate. Check your Gemini API key.')
            elif status==404:
                st.error('The configured Gemini model is unavailable. Check GEMINI_MODEL in your .env file.')
            elif status in (500,503):
                st.error('Gemini is temporarily unavailable. Try again later or enter one simple equation.')
            else:
                st.error('Could not read this question. Try entering a simple equation or check the AI configuration.')
            st.caption(f'Developer diagnostic: {type(exc).__name__}' + (f' (status {status})' if isinstance(status,int) else ''))
elif s.page=='review':
    st.header('Check and choose a question');st.write('Check that the equations match your original questions. Edit any mistakes before starting.')
    if st.button('Enter new questions',icon=':material/arrow_back:'):s.page='home';st.rerun()
    for i,q in enumerate(s.questions):
        with st.container(border=True):
            st.write(f'Question {q.get("label",i+1)}'+(' — completed' if i in s.completed else ''))
            st.write(str(q.get('text','')))
            if q.get('uncertain'):st.warning('Please check this reading carefully.')
            val=st.text_input('Equation',value=str(q.get('equation','') or ''),key=f'q_{s.nonce}_{i}')
            q['equation']=val
            try:validate_equation(clean(val));ok=True
            except Exception:ok=False;st.caption('Check the equation. Currently, only simple linear equations using x are supported.')
            resume=bool(s.steps and s.get('active')==i and clean(val)==s.steps[0])
            if st.button('Resume this question' if resume else 'Practise this question',key=f'go_{i}',disabled=not ok,type='primary'):
                if resume:s.page='solve'
                else:s.active=i;start(clean(val))
                st.rerun()
else:
    if st.button('Back to questions',icon=':material/arrow_back:'):s.page='review';st.rerun()
    current=s.steps[-1];eq=validate_equation(current);solved=simplify(eq.lhs-x)==0
    journey,work=st.columns([1,1.3],gap='large')
    with journey:
        st.subheader('Your solution journey')
        st.caption('Blue: x term · Orange: constant · Green: right side')
        for i,e in enumerate(s.steps):
            if i:st.markdown(f'<div style="text-align:center;color:#64748b">↓<br>{html.escape(s.operations[i-1])}</div>',unsafe_allow_html=True)
            st.caption('Starting equation' if i==0 else f'✓ Step {i} complete'+(' · with help' if s.revealed[i-1] else ' · your work'))
            st.markdown(equation_tiles(e,latest=i==len(s.steps)-1),unsafe_allow_html=True)
        if len(s.steps)>1 and st.button('Undo last step',icon=':material/undo:'):
            s.steps.pop();s.operations.pop();s.revealed.pop();
            if s.active in s.completed:s.completed.remove(s.active)
            reset();st.rerun()
    with work:
        if solved:
            st.success('You solved the equation!');st.latex(equation_tex(current))
            if s.active not in s.completed:s.completed.append(s.active)
            if st.button('Choose another question',type='primary'):s.page='review';st.rerun()
        else:
            if len(s.steps)>1 and not s.reveal and s.selected is None and not s.hints:
                previous=s.operations[-1]
                if s.revealed[-1]:
                    st.success(f'You’ve worked through Step {len(s.steps)-1}. Let’s try the next step!')
                else:
                    st.success(f'Correct! Step {len(s.steps)-1} complete. You chose {previous.lower()} and simplified both sides. Let’s move on to the next step!')
            st.header(f'Step {len(s.steps)}');choices=generate_operation_choices(current);random.Random(current).shuffle(choices);rec=next(c for c in choices if c['recommended'])
            if not s.reveal:
                st.write('Which operation will help you get x on its own?' if eq.lhs.subs(x,0)!=0 else 'Which operation will leave just one x on the left?')
                # Keep operation hints when the learner tries another option.
                eliminated = set(s.removed)
                cols=st.columns(2)
                for i,c in enumerate(choices):
                    with cols[i%2]:
                        if i in eliminated:
                            st.button(c['label'],key=f'eliminated_{s.nonce}_{i}',disabled=True,use_container_width=True)
                            st.caption('Eliminated — less helpful operation')
                            continue
                        if st.button(c['label'],key=f'op_{s.nonce}_{i}',type='primary' if s.selected==i else 'secondary',disabled=s.reveal,use_container_width=True):
                            s.selected=i;s.op_history.append(c["label"]);s.hints=[];s.attempts=[];s.confirm=False;st.rerun()
            choice=choices[s.selected] if s.selected is not None else None
            d=s.attempts[-1] if s.attempts else None
            stage='operation' if choice is None or not choice['recommended'] else 'correction' if d else 'arithmetic'
            if stage=='operation':
                if choice and not s.reveal:
                    st.warning('This operation keeps the equation balanced, but there is a quicker way to get x on its own. Try choosing another operation or selecting a hint.')
                    st.markdown('<span style="color:#15803d;font-size:30px">↓</span> <span style="color:#15803d">Need a clue? Try the hint below.</span>',unsafe_allow_html=True)
                s.hints=list(s.op_hints)
            if stage!='operation' and choice and not s.reveal:
                if choice['recommended']:
                    st.success('Good choice!')
                    if st.button('Change operation',key='change_operation',icon=':material/arrow_back:'):
                        s.selected=None;s.hints=list(s.op_hints);s.attempts=[];s.confirm=False;st.rerun()
                else:
                    st.warning('This operation keeps the equation balanced, but there is a quicker way to get x on its own.')
                st.write('Do the same thing to both sides. Then simplify.')
                st.latex(transformation_tex(current,choice['operation'],choice['amount']))
                answer=st.text_input('Your next equation',key=f'answer_{s.nonce}_{s.selected}',placeholder='Enter your simplified equation')
                if st.button('Check my answer',type='primary',disabled=not answer.strip(),icon=':material/check:'):
                    result=evaluate_attempt(current,choice,clean(answer))
                    if result['valid']:advance(clean(answer),choice['label'])
                    result['student_answer']=answer;s.attempts.append(result);s.hints=[];st.rerun()
                if d:st.warning(d['feedback'])
            if not s.reveal:
                st.subheader('Need help?')
                if st.button(f'Get a hint ({len(s.hints)}/3 used)',disabled=len(s.hints)>=3,key='hint_action',icon=':material/lightbulb:'):
                    level=len(s.hints)+1
                    if stage=='operation' and level==1:
                        candidates=[i for i,c in enumerate(choices) if not c['recommended']]
                        candidates.sort(key=lambda i:(i!=s.selected,not choices[i].get('eliminate_on_hint',False)))
                        s.removed=candidates[:2]
                    clue=hint_text(stage,level,choice,d,current)
                    removed_labels=[choices[i]['label'] for i in s.removed] if stage=='operation' else []
                    if stage=='operation' and level==1:
                        clue='I have removed '+ ' and '.join(removed_labels)+'. '+clue
                    with st.spinner('Preparing your hint...'):
                        ai=personalised_hint(current,stage,choice,level,s.attempts,[h[0] for h in s.hints],clue,removed_labels,s.op_history)
                    s.hints.append((ai or clue,bool(ai)))
                    if stage=='operation':
                        s.op_hints=list(s.hints)
                        if s.selected in s.removed:s.selected=None
                    st.rerun()
                if stage=='operation' and s.op_hints:
                    if s.removed:
                        st.caption('Two less helpful operations have been crossed out.')
                        if st.button('Restore options',key='restore_options',icon=':material/undo:'):
                            s.removed=[];st.rerun()
                for i,(h,ai) in enumerate(s.hints):
                    with st.container(border=True):
                        st.caption(f'Hint {i+1} · '+('AI guidance' if ai else 'Built-in guidance'));st.write(h)
                if len(s.hints)>=2 and stage!='operation':
                    c=rec if stage=='operation' else choice
                    st.markdown(balance_visual(current,c['operation'],c['amount'],d),unsafe_allow_html=True)
                if len(s.hints)==3:
                    c=rec if stage=='operation' else choice;op=c['operation'];n=c['amount']
                    if stage=='operation':
                        st.markdown(operation_clue(current),unsafe_allow_html=True)
                    elif op in ('Add','Subtract') and getattr(n,'is_Integer',isinstance(n,int)) and 0<int(n)<=20 and eq.rhs.is_Integer:
                        count=st.slider('Count the steps yourself',0,int(n),0,key=f'count_{s.nonce}_{s.selected}')
                        st.write(f'Start at {eq.rhs}. '+('← ' if op=='Subtract' else '→ ')*count+f' ({count} steps)')
                        st.caption('Where do you land?' if stage=='operation' else 'Where do you land? Enter the new equation above.')
                    elif op=='Divide':
                        st.latex(transformation_tex(current,op,n));st.write('Split both sides into the same number of equal groups. What is one group worth?')
                    if st.button('I’m stuck',key='stuck_action',icon=':material/help:'):s.confirm=True
                if s.confirm:
                    st.warning('Show the next step? This will reveal the calculation.')
                    a,b=st.columns(2)
                    if a.button('Show next step'):s.reveal=True;s.frame=0;st.rerun()
                    if b.button('Keep trying'):s.confirm=False;st.rerun()
            else:
                c=rec if stage=='operation' else choice
                new=apply_operation(current,c['operation'],c['amount'])
                frames=worked_frames(current,c['operation'],c['amount'],new)
                if st.button('Try on my own',key='cancel_reveal',icon=':material/undo:'):
                    s.reveal=False;s.confirm=False;s.frame=0;st.rerun()
                st.subheader('Let’s work through it together')
                st.caption(f'Part {s.frame+1} of {len(frames)}')
                st.progress((s.frame+1)/len(frames))
                title,visual,explanation=frames[s.frame]
                st.markdown(visual,unsafe_allow_html=True)
                st.markdown('**'+title+'**')
                st.write(explanation)
                prev,nxt=st.columns(2)
                if prev.button('Previous',disabled=s.frame==0,icon=':material/arrow_back:',use_container_width=True):
                    s.frame-=1;st.rerun()
                if nxt.button('Next',disabled=s.frame==len(frames)-1,icon=':material/arrow_forward:',type='primary',use_container_width=True):
                    s.frame+=1;st.rerun()
                if st.button('Replay explanation',icon=':material/replay:',key='replay_action'):
                    s.frame=0;st.rerun()
                if s.frame!=len(frames)-1:st.caption('Finish the explanation to continue.')
                if st.button('Continue',type='primary',disabled=s.frame!=len(frames)-1,key='continue_action',icon=':material/arrow_forward:',use_container_width=True):
                    advance(new,c['label'],True)
