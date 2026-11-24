# AlgebraStep — Functional Evaluation

## 1. Evaluation Method

Developer-led functional testing was conducted to evaluate mathematical accuracy, input validation, intelligent interaction, usability and navigation.

A total of 41 manual test cases and five automated tests were used.

- Pass: Expected behaviour achieved.
- Partial pass: Core functionality worked but required refinement.
- Fail: Expected behaviour was not achieved.

Results are cumulative across prototype iterations. Testing was conducted by the developer rather than representative GCSE students.

Reviewed repository commit:
0fef4b7cc9f110d10d91e337926c326196108942

## 2. Summary of Results

| Category | Total Tests | Initial Pass | Initial Partial Pass | Cumulative Pass |
|---|---:|---:|---:|---:|
| Mathematical accuracy | 10 | 10 | 0 | 10 |
| Input validation | 9 | 3 | 6 | 9 |
| Intelligent interaction | 12 | 12 | 0 | 12 |
| Usability and navigation | 10 | 10 | 0 | 10 |
| **Total** | **41** | **35** | **6** | **41** |

All six initially partially passing tests were successfully retested following design and implementation improvements.

## 3. Test Plan A — Mathematical Accuracy

### Objective

Evaluate whether AlgebraStep correctly supports one-step and two-step linear equations, including negative, fractional and zero solutions.

| ID | Equation | Expected Solution | Result |
|---|---|---|---|
| A01 | x + 5 = 12 | x = 7 | Pass |
| A02 | x - 4 = 9 | x = 13 | Pass |
| A03 | 4x = 20 | x = 5 | Pass |
| A04 | x/3 = 4 | x = 12 | Pass |
| A05 | 6x + 12 = 30 | x = 3 | Pass |
| A06 | 3x - 5 = 10 | x = 5 | Pass |
| A07 | 2x + 8 = 2 | x = -3 | Pass |
| A08 | 4x + 2 = 8 | x = 1.5 | Pass |
| A09 | 3x + 2 = 3 | x = 1/3 | Pass |
| A10 | 2x + 6 = 6 | x = 0 | Pass |

### Findings

All ten mathematical accuracy tests passed. These results support the decision to use deterministic mathematical reasoning through Python and SymPy rather than relying on Gemini to determine mathematical correctness.

However, the tests do not establish correctness for every possible equation.

## 4. Test Plan B — Input Validation and Extraction

### Objective

Evaluate whether the system correctly handles valid, invalid and unsupported inputs while providing understandable feedback.

| ID | Input | Expected Behaviour | Initial Result | Retest |
|---|---|---|---|---|
| B01 | Empty input | Prevent progression | Pass | Not separately recorded |
| B02 | hello / hi i need help | Identify missing equation and provide guidance | Partial pass | Pass |
| B03 | 2x + 5 | Explain missing equals sign | Partial pass | Pass |
| B04 | 2x + = 10 | Identify malformed equation | Partial pass | Pass |
| B05 | x² + 3x = 10 | Explain unsupported quadratic equation | Partial pass | Pass |
| B06 | 2x + 3 = x + 8 | Explain unsupported variables on both sides | Partial pass | Pass |
| B07 | a + 6 = 13 | Explain unsupported variable | Partial pass | Pass |
| B08 | Three pasted linear equations | Extract and allow selection of individual questions | Pass | Not separately recorded |
| B09 | Photograph containing equations | Extract questions and allow review | Pass | Not separately recorded |

### Initial Findings

Although unsupported equations were correctly rejected, the original feedback was too generic. Students were not always informed why their input was unsupported or how they could correct it.

### Design Improvements

The following changes were introduced:

- Preserved unsupported equations during AI extraction.
- Introduced specific deterministic validation messages.
- Used Gemini to personalise explanations based on the original input.
- Provided built-in feedback when Gemini was unavailable.
- Removed redundant warnings and consolidated feedback into one amber warning box.
- Standardised question numbering.

### Retesting

All six previously partially passing cases passed subsequent retesting.

This refinement supports Amershi et al.'s (2019) G1 (make clear what the system can do), G9 (support efficient correction) and G10 (scope services when in doubt).

It also supports Norman's (2013) feedback principle by helping students understand why the system rejected an input and how they can recover.

## 5. Test Plan C — Intelligent Interaction

### Objective

Evaluate proactive questioning, contextual error diagnosis, personalised hints, progressive scaffolding and interactive visual explanations.

The equation 6x + 12 = 30 was used throughout these tests.

| ID | Student Action | Expected System Behaviour | Result |
|---|---|---|---|
| C01 | Select Subtract 12 | Accept operation and enable calculation | Pass |
| C02 | Select inefficient operation | Explain that the operation maintains balance but is less efficient | Pass |
| C03 | Request first operation hint | Eliminate two inefficient choices and provide contextual guidance | Pass |
| C04 | Request second and third hints | Provide increasingly specific guidance and a visual clue | Pass |
| C05 | Attempt to request fourth hint | Prevent further hints at the current stage | Pass |
| C06 | Select Subtract 12 and request hint | Provide arithmetic-stage guidance | Pass |
| C07 | Submit 6x = 20 and request hint | Identify incorrect right-hand side and target guidance accordingly | Pass |
| C08 | Submit 6x + 2 = 18 and request hint | Identify incorrect left-hand side and target guidance accordingly | Pass |
| C09 | Submit 6x + 2 = 20 | Identify errors on both sides | Pass |
| C10 | Exhaust hints and confirm I'm stuck | Present progressive visual explanation | Pass |
| C11 | Complete 6x = 18 and request next hint | Adapt guidance to the new equation and division operation | Pass |
| C12 | Submit x = 3 after division | Recognise completion and display verified solution journey | Pass |

### Findings

All twelve intelligent interaction tests passed.

The system initiates operation-selection and calculation questions without requiring students to formulate their own prompts. Student responses provide contextual information that informs subsequent assistance.

The system successfully distinguishes between inefficient operations and incorrect mathematical calculations. It also identifies whether errors occur on the left-hand side, right-hand side or both sides of an equation.

Progressive hints provide increasingly specific support, while the worked explanation offers a learner-controlled alternative when independent attempts are unsuccessful.

These findings demonstrate the implemented functionality of:

- Mixed-initiative interaction.
- Proactive diagnostic questioning.
- Context engineering.
- Adaptive feedback.
- Progressive scaffolding.
- Learner-controlled visual explanations.
- Human-in-the-loop interaction.
- Bounded AI autonomy.

The findings also support the implementation of Amershi et al.'s (2019) G3 (time services based on context), G4 (show contextually relevant information) and G7 (support efficient invocation).

Individual AI-generated hint transcripts and AI-versus-built-in guidance labels were not systematically recorded. Therefore, these results do not establish exhaustive validation of Gemini's generated responses.

## 6. Test Plan D — Usability and Navigation

### Objective

Evaluate whether students can control the interaction, reverse actions, navigate explanations and recover from mistakes.

| ID | Student Action | Expected System Behaviour | Result |
|---|---|---|---|
| D01 | Select Home during practice | Return to welcome page | Pass |
| D02 | Return to question selection | Allow another question to be selected | Pass |
| D03 | Undo completed step | Restore previous equation and solution journey | Pass |
| D04 | Change selected operation | Return to operation selection | Pass |
| D05 | Restore eliminated options | Restore choices without refunding hints | Pass |
| D06 | Decline worked explanation | Return to independent problem-solving | Pass |
| D07 | Use Previous, Next and Replay | Display correct explanation frames and progress | Pass |
| D08 | Attempt to continue before final explanation frame | Enable Continue only after final frame | Pass |
| D09 | Inspect interface styling and disabled choices | Maintain consistent, readable controls and distinguish eliminated options | Pass |
| D10 | Complete an equation and start another | Prevent inappropriate carry-over of previous interaction state | Pass |

### Findings

All ten usability and navigation tests passed.

The interface provides reversible actions through undo, change-operation and restore-option controls. Students retain control over whether they request hints, accept worked explanations or continue independently.

Consistent button colours and labels communicate the purpose and availability of actions. Eliminated operation choices are visually crossed out rather than distinguished solely through colour.

These decisions support:

- Norman's principles of feedback, signifiers and constraints.
- Nielsen's user control and freedom heuristic.
- Recognition rather than recall.
- Amershi et al.'s G8 (support efficient dismissal).
- Amershi et al.'s G9 (support efficient correction).

These are developer-led functional checks rather than formal accessibility compliance testing or representative usability evaluation.

## 7. Automated Testing

Automated tests were implemented using pytest to check core mathematical and tutoring functionality.

Run the tests using:

`python -m pytest -q`

The automated tests were independently executed against the uploaded repository snapshot during report preparation.

Recorded output:

    .....                                    [100%]
    5 passed in 0.65s

| Automated Test | Purpose | Result |
|---|---|---|
| test_safe_parser | Accept valid expressions and reject unsupported or code-like input | Pass |
| test_choices | Generate five operation choices, one recommended operation and two choices for elimination | Pass |
| test_diagnosis | Identify correct and incorrect equation transformations | Pass |
| test_progress | Verify subtraction and division transformations | Pass |
| test_hint_relevance | Ensure correction hints target the incorrect side | Pass |

No live Gemini API requests or browser interactions were independently executed during this automated check.

## 8. Iterative Design and Development

### 8.1 Input Validation Feedback

**Problem identified:**

Generic validation messages did not explain why an equation was unsupported.

**Design change:**

Introduced specific mathematical validation and personalised AI explanations.

**Further problem identified:**

Multiple warnings and separate explanations introduced unnecessary visual clutter.

**Final refinement:**

Combined the specific error heading and personalised explanation into a single warning box.

**Outcome:**

All six previously partially passing input validation tests passed retesting.

### 8.2 Inefficient Operation Feedback

**Problem identified:**

An inefficient operation is not necessarily mathematically incorrect. Rejecting it as wrong could create misconceptions.

**Design change:**

The system acknowledges that an inefficient operation can maintain equation balance while encouraging a more direct approach.

**Outcome:**

Students receive constructive guidance without being incorrectly told that a mathematically valid operation is invalid.

### 8.3 Progressive Hint Design

**Problem identified:**

Immediately revealing the correct operation or equation could undermine independent reasoning.

**Design change:**

Introduced three progressively specific hints, elimination of inefficient choices and visual clues.

**Outcome:**

Students can request increasing levels of support while remaining responsible for completing the mathematical transformation.

### 8.4 Interactive Visual Explanations

**Problem addressed:**

Lengthy textual explanations may make mathematical transformations difficult to follow.

**Design change:**

Introduced colour-coded, progressive visual explanations with Previous, Next and Replay controls.

**Outcome:**

Students can inspect mathematical transformations at their own pace. Progression is enabled after the final explanation frame.

### 8.5 AI Reliability and Fallback

**Problem identified:**

A temporary Gemini ServerError occurred during development.

**Design change:**

Retained deterministic, built-in guidance when AI-generated feedback was unavailable.

**Outcome:**

The application continued providing assistance despite the observed API failure.

This demonstrates graceful degradation during one observed failure event, rather than comprehensive resilience testing.


## 9. Limitations and Future Development

| ID | Limitation | Proposed Improvement |
|---|---|---|
| E01 | No additional escalation of assistance after a worked explanation | Introduce alternative explanations, verified learning resources and similar practice questions |
| E02 | Limited diagnosis of underlying misconceptions | Introduce follow-up questions distinguishing arithmetic slips from conceptual misunderstandings |
| E03 | Restricted equation scope | Extend support to other variables and more complex linear equations |
| E04 | Dependence on external Gemini API | Further investigate reliability, latency and alternative deployment options |
| E05 | No persistent learner model | Adapt future assistance based on longer-term student performance |
| E06 | Generated AI explanations are not semantically verified | Introduce stronger output validation and grounding safeguards |
| E07 | Developer-led functional evaluation | Conduct representative usability and learning evaluations, subject to ethical approval |

The existing proactive questions assess operation selection and mathematical application. However, they cannot reliably establish the underlying cause of every student error.

An additional limitation identified during evaluation is that students who remain confused after completing the worked explanation cannot request alternative teaching approaches or further learning resources.

These improvements remain outside the current prototype scope.

## 10. Evaluation Conclusion

Across the development iterations, all 41 manual test cases achieved passing outcomes, including six initially partially passing input validation tests that were resolved through refinement.

All five automated tests also passed on the reviewed repository snapshot.

The evaluation supports the functional implementation of proactive questioning, contextual feedback, deterministic mathematical assessment, progressive scaffolding and interactive visual explanations.

The separation of mathematical reasoning from generative AI assistance supports the model-system boundary and limits the responsibilities assigned to the language model.

However, functional testing does not establish that AlgebraStep improves learning outcomes, reduces cognitive load or increases independent mathematical performance among GCSE students.

Further evaluation with representative users would be required to investigate these educational outcomes.


## 11. References

Amershi, S. et al. (2019) 'Guidelines for Human-AI Interaction',
Proceedings of the 2019 CHI Conference on Human Factors in
Computing Systems, pp. 1–13.
https://doi.org/10.1145/3290605.3300233

Norman, D.A. (2013) The Design of Everyday Things.
Revised and expanded edition. New York: Basic Books.
