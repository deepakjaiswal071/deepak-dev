import json
from pathlib import Path

from pydantic import ValidationError

from app.models import TestCaseCollection
from app.services.openai_client import OpenAIClient, OpenAIGenerationError

_PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "test_case_generation.md"
_PARSE_ERRORS = (json.JSONDecodeError, ValidationError)


class TestCaseGenerationError(Exception):
    """Raised when a schema-valid test case collection could not be produced."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


class TestCaseGenerationService:
    def __init__(self, client: OpenAIClient):
        self._client = client
        self._system_prompt = _PROMPT_PATH.read_text()

    def generate(self, user_story: str) -> TestCaseCollection:
        raw = self._call(user_story)
        try:
            return self._parse(raw)
        except _PARSE_ERRORS as exc:
            repair_note = (
                "Your previous response was not valid JSON matching the required "
                f"schema. Error: {exc}. Return corrected JSON only, with no extra text."
            )
            raw = self._call(user_story, repair_note=repair_note)
            try:
                return self._parse(raw)
            except _PARSE_ERRORS as exc2:
                raise TestCaseGenerationError(
                    f"Model failed to produce schema-valid output after one repair attempt: {exc2}"
                ) from exc2

    def _call(self, user_story: str, *, repair_note: str | None = None) -> str:
        try:
            return self._client.generate_test_cases(
                self._system_prompt, user_story, repair_note=repair_note
            )
        except OpenAIGenerationError as exc:
            raise TestCaseGenerationError(str(exc), status_code=exc.status_code) from exc

    @staticmethod
    def _parse(raw: str) -> TestCaseCollection:
        data = json.loads(raw)
        return TestCaseCollection.model_validate(data)
