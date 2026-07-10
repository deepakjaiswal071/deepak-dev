# AI Coding Guardrails & QA Instructions

## 1. Hallucination Prevention
- DO NOT invent UI libraries, packages, or API endpoints not defined in the architecture.
- Use native Web APIs for actions like exporting CSV files rather than introducing heavy external dependencies.
- If a technical requirement is ambiguous, stop execution and ask the user for clarification rather than assuming.

## 2. Token Optimization Guidelines
- Write compact, clean modular code. Avoid bloated comments or repeating code blocks across multiple files.
- Design the backend to request minimal, strict JSON tokens from the upstream LLM by leveraging JSON Mode or Structured Outputs.

## 3. QA Expert Rules
- Generated test cases MUST include distinct classifications: `Positive`, `Negative`, and `Boundary Value Analysis (BVA)`.
- Test steps must be concrete actions (e.g., "Click the Submit button"), never vague descriptions.
