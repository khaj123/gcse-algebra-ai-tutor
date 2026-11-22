
import streamlit as st
from sympy import latex
from src.math_checker import parse_equation
from src.operations import apply_operation

st.set_page_config(
    page_title="AlgebraStep",
    page_icon="📘",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #F7F9FC;
}
h1 {
    color: #2447A5;
}
</style>
""", unsafe_allow_html=True)

st.title("📘 AlgebraStep")
st.caption("Your interactive GCSE algebra tutor")

if "steps" not in st.session_state:
    st.session_state.steps = []

if "operations" not in st.session_state:
    st.session_state.operations = []

st.info(
    "👋 Hi! Do you have an algebra question "
    "you'd like help with?"
)

equation_input = st.text_input(
    "Enter your equation",
    placeholder="2x + 3 = 11"
)

if st.button("Start solving", type="primary"):
    try:
        parsed = parse_equation(equation_input)
        st.session_state.steps = [equation_input]
        st.session_state.operations = []
        st.success("Equation accepted!")
    except Exception as error:
        st.error(f"Please check your equation: {error}")

if st.session_state.steps:

    st.divider()
    st.subheader("Your solution graph")

    for index, step in enumerate(st.session_state.steps):

        equation = parse_equation(step)

        st.latex(
            latex(equation.lhs)
            + " = "
            + latex(equation.rhs)
        )

        if index < len(st.session_state.operations):
            st.markdown(
                "⬇️ **"
                + st.session_state.operations[index]
                + "**"
            )

    st.divider()

    current_equation = st.session_state.steps[-1]

    st.subheader("What should we do next?")

    operation = st.selectbox(
        "Choose an operation",
        ["Subtract", "Add", "Divide", "Multiply"]
    )

    amount = st.number_input(
        "Enter a number",
        value=3.0,
        step=1.0
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Apply operation", type="primary"):
            try:
                new_equation = apply_operation(
                    current_equation,
                    operation,
                    amount
                )

                st.session_state.steps.append(new_equation)
                st.session_state.operations.append(
                    f"{operation} {amount:g} on both sides"
                )

                st.rerun()

            except Exception as error:
                st.error(str(error))

    with col2:
        if st.button("💡 Hint"):
            st.info(
                "Think about which operation would "
                "help isolate x."
            )

    with col3:
        if st.button(
            "↩️ Undo",
            disabled=len(st.session_state.steps) <= 1
        ):
            st.session_state.steps.pop()
            st.session_state.operations.pop()
            st.rerun()
