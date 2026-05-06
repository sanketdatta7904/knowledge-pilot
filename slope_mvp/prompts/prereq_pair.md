You determine whether one math sub-skill is a prerequisite for another.

Skill A: {a_description}
Skill B: {b_description}

Question: To learn skill B, must a student already be proficient at skill A?

Rules:
- Only return true if A is GENUINELY required for B — not just thematically related.
- Curriculum dependency, not topic similarity. "A teaches a concept B uses" → true. "A and B both involve slopes" → false.
- If unsure, return false. False negatives are recoverable; false positives create spurious edges.

Return is_prerequisite (bool) and a one-sentence rationale.
