# AlgebraStep

**README prose word count:** Approximately 750 words
(excluding setup commands and configuration).

AlgebraStep is an intelligent interactive GCSE algebra tutor combining proactive diagnostic questioning, contextual AI guidance and progressive visual explanations to support independent mathematical reasoning.

## Project Status

### Implemented Features

- Typed equations, pasted questions and photograph extraction.
- Editable question review and selection.
- System-initiated operation-selection and calculation questions.
- Deterministic mathematical checking and side-specific error feedback.
- Progressive, contextually personalised hints.
- Elimination of inefficient operation choices.
- Colour-coded solution journey displaying previous transformations.
- Interactive worked explanations with learner-controlled navigation.
- Undo, change-operation, restore-option and question navigation controls.
- Personalised input validation feedback.

The prototype supports simple one-step and two-step linear equations in x, with x only on the left-hand side.

Gemini-dependent question extraction requires a working API connection. Simple typed equations and built-in guidance remain usable without it.

No simulated AI responses are presented as live AI.

### Planned Features

- Deeper diagnosis of underlying mathematical misconceptions.
- Alternative explanations and additional learning resources.
- Support for more complex equations and other variables.
- Graph visualisations and related practice questions.

These features remain outside the current prototype scope.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and interaction controller |
| Streamlit | User interface, widgets and session state |
| HTML/CSS | Custom interface styling |
| LaTeX | Mathematical notation and visual explanations |
| SymPy | Deterministic mathematical validation, transformations and error diagnosis |
| Google Gen AI SDK | Gemini integration for question extraction and personalised guidance |
| python-dotenv | Loading local environment variables |
| pytest | Automated functional testing |

The default AI model is `gemini-3.5-flash-lite`, configurable through the `GEMINI_MODEL` environment variable.

Mathematical correctness is determined independently of Gemini through SymPy.

## Running the Application

The following instructions are for Windows PowerShell.

### 1. Clone the repository

```powershell
git clone https://github.com/khaj123/gcse-algebra-ai-tutor.git
cd gcse-algebra-ai-tutor
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Gemini

Create a file named `.env` in the root of the repository.

```dotenv
GEMINI_API_KEY=your_own_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Reviewers must supply their own Google Gemini API key.

Never commit API keys or the `.env` file to GitHub.

Model availability depends on the reviewer's API account. Avoid including personal information in uploaded questions, as content may be sent to Gemini for processing.

### 5. Launch AlgebraStep

```powershell
python -m streamlit run app.py
```

### 6. Run automated tests

```powershell
python -m pytest -q
```

## Development Record

The following development record documents significant design decisions, implementation stages, problems identified during development and testing, and subsequent refinements.

### Understanding the Test References

Individual test case identifiers referenced throughout this development record correspond to the [Functional Evaluation](docs/evaluation.md).

| Test Identifiers | Testing Category | Supporting Documentation |
|---|---|---|
| A01–A10 | Mathematical accuracy | [Test Plan A](docs/evaluation.md#3-test-plan-a--mathematical-accuracy) |
| B01–B09 | Input validation and extraction | [Test Plan B](docs/evaluation.md#4-test-plan-b--input-validation-and-extraction) |
| C01–C12 | Intelligent interaction | [Test Plan C](docs/evaluation.md#5-test-plan-c--intelligent-interaction) |
| D01–D10 | Usability and navigation | [Test Plan D](docs/evaluation.md#6-test-plan-d--usability-and-navigation) |

The evaluation document contains individual test inputs, expected behaviour, results, retesting outcomes and limitations.

### 1. Initial Design and Planning

Assignment 1 literature informed the decision to combine guided questioning with interactive visual explanations. The prototype was restricted to GCSE linear equations to maintain a manageable scope.

Relevant commits:

- [4392e6f — Literature-informed interface design decisions](https://github.com/khaj123/gcse-algebra-ai-tutor/commit/4392e6f)
- [0c642e2 — Initial functional requirements and prototype scope](https://github.com/khaj123/gcse-algebra-ai-tutor/commit/0c642e2)
- [7df2afd — Completed functional requirements](https://github.com/khaj123/gcse-algebra-ai-tutor/commit/7df2afd)
- [5e86e27 — Literature-grounded interaction flow](https://github.com/khaj123/gcse-algebra-ai-tutor/commit/5e86e27)

### 2. Developing the Mathematical Core

I separated mathematical assessment from AI-generated guidance to reduce reliance on potentially incorrect LLM outputs.

SymPy was used to validate equations, check transformations and identify incorrect sides. Interactive operations and solution history were subsequently introduced.

Verification: All ten mathematical accuracy tests passed ([Test Plan A, A01–A10](docs/evaluation.md#3-test-plan-a--mathematical-accuracy)).

Relevant commits:

- [6ea9f2a — Initial SymPy equation equivalence checker](https://github.com/khaj123/gcse-algebra-ai-tutor/commit/6ea9f2a)
- [40f8476 — Interactive algebra operations and solution history](https://github.com/khaj123/gcse-algebra-ai-tutor/commit/40f8476)

### 3. Design Refinements During Development

#### 3.1 Refining Feedback for Inefficient Operations

**Problem identified:** Rejecting an inefficient operation risked incorrectly suggesting that it was mathematically invalid.

**Design refinement:** I changed the feedback to acknowledge that the operation maintains equation balance while encouraging a quicker approach to isolating x.

**Verification:** [Test Plan C, C02](docs/evaluation.md#5-test-plan-c--intelligent-interaction) confirmed that inefficient operations received constructive feedback.

#### 3.2 Improving Contextual Hint Relevance

**Problem identified:** Early hints were too generic or repetitive and did not sufficiently address individual mistakes.

**Design refinement:** I refined Gemini's prompts to include the current equation, selected operation, previous attempts, diagnosed errors, eliminated choices and previous hints.

**Verification:** [Test Plan C, C03–C09 and C11](docs/evaluation.md#5-test-plan-c--intelligent-interaction) checked progressive guidance, error-specific feedback and adaptation to updated equations.

#### 3.3 Refining Progressive Scaffolding

**Problem identified:** Revealing answers too early could undermine independent reasoning.

**Design refinement:** I introduced three increasingly specific hints, elimination of inefficient choices and visual clues before offering a worked explanation.

**Verification:** [Test Plan C, C03–C05](docs/evaluation.md#5-test-plan-c--intelligent-interaction) confirmed hint progression, elimination of choices and the hint limit.

#### 3.4 Improving Learner Control

**Problem identified:** Students needed greater control over the pace of explanations and opportunities to reconsider their decisions.

**Design refinement:** I introduced Previous, Next and Replay controls, confirmation before revealing a step, undo and change-operation controls.

**Verification:** [Test Plan C, C10](docs/evaluation.md#5-test-plan-c--intelligent-interaction) and [Test Plan D, D03–D08](docs/evaluation.md#6-test-plan-d--usability-and-navigation) checked explanation navigation, reversibility and learner control.

The resulting intelligent interaction and visual explanation functionality is recorded in:

- [73f04d1 — Implement contextual AI tutoring, interactive visual explanations and accessible UI](https://github.com/khaj123/gcse-algebra-ai-tutor/commit/73f04d1)

### 4. Design Refinements Following Formal Testing

#### 4.1 Improving Input Validation and Error Recovery

**Initial testing outcome:** Six of nine input validation tests initially partially passed. Unsupported inputs were correctly rejected, but generic feedback did not explain why.

**Design refinement:** I preserved unsupported expressions during extraction, introduced specific deterministic validation reasons and used Gemini to personalise explanations.

**Retesting outcome:** All six initially partially passing tests subsequently passed.

Supporting evidence: [Test Plan B, B02–B07](docs/evaluation.md#4-test-plan-b--input-validation-and-extraction).

#### 4.2 Reducing Visual Clutter

**Problem identified:** Separate warnings and personalised explanations created unnecessary visual clutter.

**Design refinement:** I consolidated validation feedback into a single amber warning box, removed redundant warnings and standardised question numbering.

**Verification:** Reviewed the revised interface and confirmed that personalised validation feedback appeared within a single warning.

Supporting evidence: [Test Plan B](docs/evaluation.md#4-test-plan-b--input-validation-and-extraction).

#### 4.3 Maintaining Assistance During AI Failure

**Problem identified:** A temporary Gemini ServerError occurred during personalised feedback testing.

**Design refinement:** Built-in guidance was retained so that assistance remained available when AI-generated feedback failed.

**Verification:** Observed fallback behaviour during the API failure.

This demonstrates graceful degradation during an observed failure rather than comprehensive reliability testing.

#### 4.4 Improving Interface Consistency

**Problem identified:** Inconsistent button styling could make available actions and interaction states less clear.

**Design refinement:** I standardised button colours, selected states and disabled operation choices. Eliminated options were crossed out rather than distinguished solely through colour.

**Verification:** [Test Plan D, D09](docs/evaluation.md#6-test-plan-d--usability-and-navigation) confirmed interface consistency.

The validation and interface styling refinements are recorded in:

- [0fef4b7 — Improve validation with personalised AI feedback and consistent interface styling](https://github.com/khaj123/gcse-algebra-ai-tutor/commit/0fef4b7)

The [full commit history](https://github.com/khaj123/gcse-algebra-ai-tutor/commits/main/) documents the progression from initial planning to implementation and post-testing refinement.

## Evaluation Results

Developer-led functional testing produced the following cumulative results:

| Testing Category | Total Tests | Initial Passes | Initial Partial Passes | Cumulative Passes |
|---|---:|---:|---:|---:|
| Mathematical accuracy | 10 | 10 | 0 | 10 |
| Input validation and extraction | 9 | 3 | 6 | 9 |
| Intelligent interaction | 12 | 12 | 0 | 12 |
| Usability and navigation | 10 | 10 | 0 | 10 |
| **Total manual tests** | **41** | **35** | **6** | **41** |

Five automated tests also passed during development.

All six initially partially passing input validation tests were successfully retested following design refinements.

B01, B08 and B09 passed earlier in development, but separate final regression results were not recorded.

See the [Functional Evaluation](docs/evaluation.md) for detailed test cases, expected behaviour, results, development refinements and limitations.

These developer-led functional checks do not establish improved learning outcomes, reduced cognitive load or increased independent mathematical performance among GCSE students.

Representative user evaluation remains future work.

## AI Assistance and Authorship

I used ChatGPT to assist with Python implementation, debugging, interface development, test planning, documentation and architecture/storyboard preparation.

I reviewed and adapted AI-generated suggestions by running the application, checking mathematical examples, testing interactions and identifying design problems.

Examples of my involvement include:

- Identifying repetitive hints and requesting more focused, contextually relevant guidance.
- Recognising that inefficient operations should not be described as mathematically incorrect.
- Identifying generic validation warnings and requesting explanations of specific input problems.
- Recognising unnecessary visual clutter and consolidating validation feedback.
- Requesting consistent interface styling and improved learner controls.
- Conducting manual testing and retesting revised functionality.

Gemini is also used at runtime for question extraction and personalised tutoring guidance.

Mathematical correctness is determined independently through SymPy. AI-generated explanations are not independently semantically verified.

The visual design draws inspiration from Zhou et al.'s iGraph research rather than reusing their implementation.

## Additional Documentation

| Document | Purpose |
|---|---|
| [Design decisions](docs/design-decisions.md) | Original literature-informed interface design decisions |
| [Interaction flow](docs/interaction-flow.md) | Planned interaction scenarios and student journeys |
| [Requirements](docs/requirements.md) | Original functional and non-functional requirements |
| [Functional evaluation](docs/evaluation.md) | Test cases, results, iterative improvements and limitations |

The original planning documents include proposed features that were not implemented in the final prototype.

## Project Structure

- `app.py` — Main application and interaction controller.
- `src/` — Mathematical checking, operation generation, tutoring, AI integration and visualisation modules.
- `tests/test_tutor.py` — Automated functional tests.
- `docs/` — Design, requirements, interaction and evaluation documentation.
- `requirements.txt` — Python dependencies.
- `.streamlit/` — Interface theme configuration.