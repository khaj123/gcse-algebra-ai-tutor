
# Interface Design Decisions

## 1. Welcome Screen

**Design Decision:** Explain what the tutor does, the algebra topics it supports and its limitations before the student begins.

**Rationale:** Luger and Sellen (2016) identify the expectation gulf, where users overestimate the capabilities of conversational AI. Amershi et al. (2019) recommend clearly communicating what an AI system can do.

## 2. Opening Interaction

**Design Decision:** The AI initiates the interaction by introducing an algebra problem and asking a diagnostic question.

**Rationale:** Horvitz (1999) supports mixed-initiative interaction, where the system can initiate appropriate actions rather than waiting for user instructions. This also addresses the research gap identified in the literature review.

## 3. Reasoning Layout

**Design Decision:** Display algebraic transformations as vertically connected reasoning blocks, inspired by Zhou et al.'s iGraph interface.

**Rationale:** Zhou et al. (2026) found that interactive visual explanations helped participants identify incorrect steps in AI-generated reasoning. This project explores applying a similar approach to GCSE algebra learning.

## 4. Colour-Coded Terms

**Design Decision:** Use consistent colours to represent corresponding mathematical terms across equation transformations.

**Rationale:** Zhou et al. (2026) reported positive or neutral participant responses to consistent colour-coding. This decision also draws on the importance of visual attention and perceptual cues, using the same colours allows students to associate certain transformations with a colour making it easier to follow and recognise certain transformations instead of relying on recall.

## 5. Labelled Operations

**Design Decision:** Display clearly labelled mathematical operations, such as "Subtract 3 from both sides", instead of relying on symbols alone.

**Rationale:** Norman (2008, 2013) emphasises signifiers that communicate available actions. Supported by the concept of recognition over recall, reducing the need for students to remember possible operations.

## 6. Tutor Language

**Design Decision:** Use short, age-appropriate, encouraging and mathematically precise questions and explanations.

**Rationale:** Grice's (1975) maxims of quantity, relation and manner support clear and relevant communication. This aims to reduce unnecessary cognitive load.

## 7. Screen Positioning

**Design Decision:** Position the current equation and available operations close together, with the active step visually emphasised.

**Rationale:** Based on selective attention and visual perception. Grouping related information and highlighting the current step aims to help students focus on the relevant mathematical task. The layout will require usability testing.

## 8. Error Feedback

**Design Decision:** Explain incorrect operations, generate a targeted follow-up question and allow students to retry before revealing a worked solution.When a student makes an incorrect algebraic transformation, the tutor will explain the mistake using LLM-generated feedback grounded in the mathematical checker's result. It will then ask a targeted follow-up
question and allow the student to retry before revealing a worked solution.

**Rationale:** Bastani et al. (2025) highlight the risks of unrestricted AI assistance for independent learning. Moreover this draws on the concept of conversational repair, supporting clarification and correction rather than simply reporting an error.

## 9. Hint Controls

**Design Decision:** Provide progressive hints, beginning with small clues or guiding questions before offering more explicit explanations.Include a "hint" button that students can use when they're stuck.Hints will be progressive starting with a question or small clue before offering more explicit guidance. The tutor will not immediately reveal the complete solution.


**Rationale:** The literature review identifies the importance of scaffolding while recognising that excessive guidance may reduce student independence. Choi and Chang (2025) discuss Socratic questioning as a guided tutoring approach.

## 10. Progress and Control

**Design Decision:** Display visible progress through the equation and provide undo, retry and clarification controls. Students can also challenge the AI's interpretation of their answers.The tutor will display the student's current position within the equation-solving process using vertically connected iGraph-inspired reasoning blocks.

**Rationale:** Norman (2013) emphasises feedback and reducing the gulf of evaluation, visible feedback allows users to understand what happened after an
action. Amershi et al. (2019) recommend supporting user correction. The aspects of visibility and reversibility need to be takenn into consideration.

## 11. Limitations During Use

**Design Decision:** Politely redirect requests outside the tutor's supported scope and explain that external application integrations are unavailable.For example, if a student asks about an unrelated subject or requests integration with another application,the tutor will explain that it currently supports GCSE
linear equations and cannot connect to external services.The tutor will then offer a relevant algebra activity to help the student continue learning.

**Rationale:** Luger and Sellen (2016) describe the expectation gulf associated with conversational AI. This aims to decline unsupported requests as a form of conversational repair while returning control to the user.This decision aims to prevent students from assuming that a fluent conversational interface has unrestricted knowledge or access to external applications.

## 12. Data and Memory

**Design Decision:** Maintain minimal learning state, such as the current equation, previous attempts and possible misconceptions. Allow students to inspect and correct the AI's interpretations, avoiding unnecessary long-term profiling.

**Rationale:**  AI memory should be inspectable, editable and forgettable. Keeping learning state minimal and correctable aims to reduce privacy risks and prevent incorrect or outdated inferences from influencing future feedback.
