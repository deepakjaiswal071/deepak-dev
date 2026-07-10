import json
import time
from pathlib import Path
from typing import Any

from openai import APIError, APIStatusError, APITimeoutError, OpenAI

from app.config import Settings

# Vendored copy of .claude/schema.json — kept in sync by test_schema_sync.py.
# Loaded relative to this package (not the repo root) so the client works
# unchanged whether the whole repo or just backend/ is deployed.
_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema.json"
_MAX_ATTEMPTS = 2
_REQUEST_TIMEOUT_SECONDS = 20


class OpenAIGenerationError(Exception):
    """Raised when the OpenAI API call ultimately fails."""

    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


class OpenAITimeoutError(OpenAIGenerationError):
    def __init__(self, message: str):
        super().__init__(message, status_code=504)


def _load_response_schema() -> dict[str, Any]:
    with _SCHEMA_PATH.open() as f:
        schema = json.load(f)
    _enforce_strict(schema)
    return schema


def _enforce_strict(node: Any) -> None:
    """OpenAI's strict Structured Outputs mode requires every object node to
    set additionalProperties=false and list every property as required."""
    if isinstance(node, dict):
        if node.get("type") == "object" and "properties" in node:
            node.setdefault("additionalProperties", False)
            node["required"] = list(node["properties"].keys())
        for value in node.values():
            _enforce_strict(value)
    elif isinstance(node, list):
        for item in node:
            _enforce_strict(item)


class OpenAIClient:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._schema = _load_response_schema()

    def generate_test_cases(
        self, system_prompt: str, user_story: str, *, repair_note: str | None = None
    ) -> str:
        messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_story},
        ]
        if repair_note:
            messages.append({"role": "user", "content": repair_note})

        last_error: Exception | None = None
        for attempt in range(1, _MAX_ATTEMPTS + 1):
            try:
                response = self._client.chat.completions.create(
                    model=self._settings.openai_model,
                    messages=messages,  # type: ignore[arg-type]
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "test_case_collection",
                            "schema": self._schema,
                            "strict": True,
                        },
                    },
                    timeout=_REQUEST_TIMEOUT_SECONDS,
                )
                return response.choices[0].message.content or ""
            except APITimeoutError as exc:
                last_error = exc
                if attempt == _MAX_ATTEMPTS:
                    raise OpenAITimeoutError(str(exc)) from exc
            except APIStatusError as exc:
                last_error = exc
                if exc.status_code == 401 or attempt == _MAX_ATTEMPTS:
                    raise OpenAIGenerationError(str(exc)) from exc
            except APIError as exc:
                last_error = exc
                if attempt == _MAX_ATTEMPTS:
                    raise OpenAIGenerationError(str(exc)) from exc
            time.sleep(2 ** (attempt - 1))

        raise OpenAIGenerationError(str(last_error))
