# AI Test Case Generator

Paste an Agile user story (persona, goal, benefit, and acceptance criteria) into the
web UI and get back structured Positive / Negative / Boundary test cases.

- `backend/` — FastAPI service that calls the OpenAI API with Structured Outputs to
  produce test cases strictly matching [`.claude/schema.json`](.claude/schema.json).
- `frontend/` — React (Vite + Tailwind) single-page UI: paste a story, view the
  generated test cases, export as CSV or JSON.
- `.claude/` — the product contract this app is built against (`plan.md`,
  `schema.json`, `instructions.md`, `workflow.md`).

The app is stateless: nothing is persisted server-side. Generated test cases live
only in the browser tab until you export them.

## Running locally

### Backend

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env   # fill in OPENAI_API_KEY
.venv/bin/uvicorn app.main:app --reload --port 8000
```

Run tests with `.venv/bin/pytest`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # defaults to http://localhost:8000
npm run dev
```

Open the printed local URL (default `http://localhost:5173`). The backend must be
running for generation requests to succeed.

## How generation works

The backend loads a single versioned prompt template
(`backend/app/prompts/test_case_generation.md`) that encodes the QA rules from
`.claude/instructions.md` — every acceptance criterion gets Positive coverage, plus
Negative/Boundary coverage where the criterion implies validation, a limit, or a
conditional UI state. The OpenAI call uses Structured Outputs constrained to
`.claude/schema.json`, and the backend validates the response against that schema,
retrying once with a corrective prompt before failing cleanly. Editing the prompt
template is the single place to tune behavior for future user stories.
