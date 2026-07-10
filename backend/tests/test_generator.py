import json
from unittest.mock import MagicMock

import pytest

from app.services.openai_client import OpenAIGenerationError, OpenAITimeoutError
from app.services.test_case_generator import TestCaseGenerationError, TestCaseGenerationService

VALID_PAYLOAD = json.dumps(
    {
        "test_cases": [
            {
                "id": "TC-001",
                "scenario": "User logs in with valid credentials",
                "preconditions": "User has a registered account",
                "steps": ["Enter valid email", "Enter valid password", "Click Sign-In"],
                "expected_result": "User is redirected to the homepage in a logged-in state",
                "type": "Positive",
            }
        ]
    }
)


def _make_service(client: MagicMock) -> TestCaseGenerationService:
    return TestCaseGenerationService(client)


def test_generate_returns_valid_collection_on_first_try():
    client = MagicMock()
    client.generate_test_cases.return_value = VALID_PAYLOAD
    service = _make_service(client)

    result = service.generate("As a user I want to log in...")

    assert len(result.test_cases) == 1
    assert result.test_cases[0].type == "Positive"
    client.generate_test_cases.assert_called_once()


def test_generate_repairs_once_on_invalid_json_then_succeeds():
    client = MagicMock()
    client.generate_test_cases.side_effect = ["not json", VALID_PAYLOAD]
    service = _make_service(client)

    result = service.generate("story")

    assert len(result.test_cases) == 1
    assert client.generate_test_cases.call_count == 2


def test_generate_raises_after_repair_still_invalid():
    client = MagicMock()
    client.generate_test_cases.side_effect = ["not json", "still not json"]
    service = _make_service(client)

    with pytest.raises(TestCaseGenerationError):
        service.generate("story")


def test_generate_wraps_openai_errors_as_502():
    client = MagicMock()
    client.generate_test_cases.side_effect = OpenAIGenerationError("boom")
    service = _make_service(client)

    with pytest.raises(TestCaseGenerationError) as exc_info:
        service.generate("story")
    assert exc_info.value.status_code == 502


def test_generate_wraps_timeout_as_504():
    client = MagicMock()
    client.generate_test_cases.side_effect = OpenAITimeoutError("timed out")
    service = _make_service(client)

    with pytest.raises(TestCaseGenerationError) as exc_info:
        service.generate("story")
    assert exc_info.value.status_code == 504
