
# AlgebraStep — Student Interaction Flow

## Development Status
Planned interaction design. Features will be marked as
implemented, simulated or planned during development.

## Scenario 1 — Student Submits an Algebra Homework Question

1. The student opens AlgebraStep.
2. The AI tutor asks:
   "Hi! Do you have an algebra question you'd like help with?"
3. The student either:
   - Types an equation.
   - Uploads an image of their homework question.
4. The system interprets the equation and displays it.
5. The student confirms or corrects the interpretation.
6. The LLM asks:
   "What do you think the first step should be?"
7. The student selects or enters an algebraic operation.
8. The mathematical checker verifies the transformation.
9. If valid:
   - A new equation node appears in the iGraph.
   - An arrow displays the operation (e.g. −3, ÷2).
   - Each mathematical term retains its colour.
   - The AI asks the next diagnostic question.
10. The student continues until the equation is solved.
11. The tutor confirms the verified solution.
12. The completed iGraph remains available for review.

## Scenario 2 — Student Makes an Incorrect Attempt

1. The student selects an incorrect operation.
2. The mathematical checker evaluates the attempt.
3. The attempted answer remains visible as feedback.
4. The verified iGraph does not advance.
5. The LLM explains the mistake and asks a
   diagnostic follow-up question.
6. The student can:
   - Retry the operation.
   - Request a hint using a blue Hint button.
   - Undo a previous verified step.
7. If the student continues to struggle, the tutor
   offers additional explanations or practice.
8. Once the student performs a valid transformation,
   the iGraph advances.

## Scenario 3 — Visual Hints and Additional Support

1. The student clicks the blue Hint button.
2. The tutor provides a progressive hint.
3. The student can request a graphical explanation.

4. Balance-scale visualisation:
   - Shows the two sides of the equation.
   - Demonstrates why operations must be applied
     equally to both sides.

5. Coordinate graph visualisation:
   - Plots the relevant linear equation.
   - Uses colours consistent with the algebraic terms.
   - Labels the x-intercept and y-intercept.
   - Displays the gradient.
   - For equations such as 2x + 3 = 11, plots
     y = 2x + 3 and y = 11.
   - Highlights their intersection as the solution.

6. The student may access a short instructional
   animation or video when available.

7. If the student repeatedly makes a mistake,
   the tutor may generate a related practice question.

8. The student can return to their original
   homework equation at any time.

## Scenario 4 — Clarification and Scope Boundaries

1. The student asks for clarification or challenges
   the tutor's interpretation.
2. The tutor uses the current equation and verified
   learning state to respond.
3. The student can correct a misinterpreted equation.
4. If the request is outside supported GCSE linear
   equations, the tutor explains its limitations.
5. The tutor offers to return to the current
   algebra question.


## Key Design Principles 

- **Mixed-initiative interaction — Horvitz (1999):**
The AI proactively asks diagnostic questions while allowing the student to control their learning.

- **Interactive visual reasoning — Zhou et al. (2026):**
Inspired by iGraph, AlgebraStep uses connected, colour-coded equation nodes to make mathematical transformations visible and inspectable.

- **Independent learning — Bastani et al. (2025):**
Students attempt algebraic operations before receiving solutions, encouraging active reasoning rather than dependence on AI-generated answers.

- **Working Memory Model — Baddeley and Hitch (1974):**
Step-by-step explanations, diagrams and visual representations aim to reduce unnecessary working-memory demands.

- **Signifiers, feedback and recovery — Norman (2013):**
Clearly labelled Hint, Retry and Undo buttons, alongside immediate feedback, make the interaction understandable and reversible.

- **Conversational grounding — Clark and Brennan (1991):**
The tutor confirms its interpretation of the student's homework equation before proceeding.

- **Conversational repair — Schegloff, Jefferson and Sacks (1977):**
Students can correct misunderstood questions,request clarification and challenge AI responses.

- **Human-AI interaction guidelines —Amershi et al. (2019):**
The interface communicates its capabilities,supports correction and gives students control over AI assistance.

- **LLM reliability — Ji et al. (2023):**
Because language models can generate inaccurate information, AlgebraStep uses an independent mathematical checker to verify transformations.

- **Context management — Liu et al. (2024):**
The tutor supplies relevant equation state,verified steps and recent attempts as context, while avoiding unnecessary information.

- **Tool-augmented language models Schick et al. (2023):**
AlgebraStep separates LLM-generated tutoring dialogue from mathematical checking performed by application code and SymPy.

- **Human-centred AI — Shneiderman (2022):**
The student retains control over progression,hints, corrections and the solving process.


## Implementation Priorities

### Core Features
- Typed equation input.
- Image upload and equation interpretation.
- LLM-generated diagnostic questions.
- Independent mathematical verification.
- Interactive colour-coded iGraph.
- Correct and incorrect operation feedback.
- Hint, Retry and Undo controls.
- Balance-scale and coordinate graph explanations.

### Additional Features
- Instructional videos and animations.
- Related practice questions.
- More advanced misconception tracking