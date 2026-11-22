
# AlgebraStep — Functional Requirements and Scope

## 1. Project Aim

To develop an intelligent interactive GCSE algebra tutor
that combines LLM-generated diagnostic questioning with
interactive, iGraph-inspired visual explanations.

The system aims to support students in understanding
algebraic transformations and solving equations
independently rather than simply relying on AI generated answers without testing they have fully understood each explanation.For example, if a student uses AlgebraStep for their homework our system will not simply give them answers, it will check their understanding before fully revealing the answer and provide a step by step guide to completing the answer themselves.

## 2. Target Users

Secondary-school students studying GCSE mathematics,
particularly those who struggle with solving linear
equations or understanding the reasoning behind
algebraic operations.

## 3. Prototype Scope

The initial prototype will support one-variable linear
equations, focusing on one-step and two-step problems.

Example:
2x + 3 = 11

The system will demonstrate a complete tutoring
interaction from the initial diagnostic question
through to solving the equation.

## 4. Functional Requirements

### FR01 — Communicate Capabilities and Limitations
The welcome screen must explain:
- What AlgebraStep does.
- Which algebra topics are supported.
- How the AI helps students learn.
- What the system cannot do.

### FR02 — System-Initiated Interaction
The LLM must initiate the tutoring session by introducing an equation and generating a diagnostic question. Or the LLM initiates a message asking which algerba problem a student needs help with "Hi there, do you have a linear algebra problem you need help solving?"

The student should not need to formulate an initial help request.

### FR03 — Student-Controlled Operations
Students must attempt an algebraic operation before the system progresses to the next equation step.

The interface must display clearly labelled operations rather than relying on symbols alone.

### FR04 — Mathematical Verification
The application must check whether the student's attempted transformation is mathematically valid.

The LLM must receive the verification result before generating feedback.

### FR05 — Adaptive Diagnostic Feedback
The LLM must generate targeted questions and
explanations based on:
- The current equation.
- The student's attempted operation.
- The mathematical verification result.
- Relevant previous attempts.

### FR06 — iGraph-Inspired Visualisation
The interface must display:
- Vertically connected equation steps.
- Clearly labelled operations.
- Consistent colour-coding of corresponding terms.
- The current step highlighted.
- Previous steps remaining visible.

### FR07 — Error Recovery
When an operation is incorrect:
- Explain the mistake.
- Ask a targeted follow-up question.
- Allow the student to retry.
- Do not automatically progress to the next step.

### FR08 — Progressive Hints
Students must be able to request hints.

Hints should become progressively more explicit while preserving opportunities for independent problem-solving.

### FR09 — Visible Progress and Control
Students must be able to:
- View their progress through the equation.
- Retry an incorrect operation.
- Undo a previous step.
- Request clarification.
- Challenge the AI's interpretation.

### FR10 — Scope Enforcement
The system must recognise unsupported requests and explain its limitations.

It must not claim to access external applications or perform actions it cannot execute.

### FR11 — Session Context
The application must maintain the information needed for the current tutoring session:
- Current equation.
- Completed transformations.
- Previous student attempts.
- Possible misconceptions.

Inferred misconceptions must be treated as provisional and correctable.

## 5. Non-Functional Requirements

### NFR01 — Mathematical Reliability
Mathematical correctness must be checked independently of the LLM.

### NFR02 — Usability
The interface should use clear signifiers, readable text, consistent colours and visible feedback.

### NFR03 — Transparency
Students should understand what the AI can do, what it is doing and when it is
uncertain.

### NFR04 — Privacy
The prototype should avoid collecting unnecessary personal information and
unnecessary persistent student profiles.

### NFR05 — Responsiveness
The interface should acknowledge student 5actions promptly and indicate when an
LLM response is being generated.

## 6. Out of Scope

The initial prototype will not support:
- All GCSE mathematics topics.
- Quadratic or simultaneous equations.
- Integration with school systems.
- Automatic homework submission.
- Long-term student profiling.
- Unrestricted general-purpose AI assistance.

## 7. Planned Evaluation

The prototype will be evaluated using
representative interaction scenarios:

1. A student correctly solves an equation.
2. A student makes an incorrect transformation.
3. A student requests progressive hints.
4. A student challenges an AI interpretation.
5. A student asks an unsupported question.

Testing will examine mathematical correctness,
LLM behaviour, visual consistency, error
recovery and capability boundaries.

## 8. Development Status

All requirements are currently proposed.

Implementation and testing status will be
updated as development progresses.
