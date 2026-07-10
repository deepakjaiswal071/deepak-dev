from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app
from app.models import TestCase, TestCaseCollection
from app.services.test_case_generator import TestCaseGenerationError

client = TestClient(app)

_VALID_STORY = (
    "As a Returning Customer, I want to log in using my email/phone number "
    "and password, so that I can access my account and order history."
)


def test_generate_test_cases_success():
    fake_generator = MagicMock()
    fake_generator.generate.return_value = TestCaseCollection(
        test_cases=[
            TestCase(
                id="TC-001",
                scenario="Valid login",
                preconditions="Registered user exists",
                steps=["Enter credentials", "Click Sign-In"],
                expected_result="User reaches homepage logged in",
                type="Positive",
            )
        ]
    )
    app.state.generator = fake_generator

    response = client.post("/api/generate-test-cases", json={"user_story": _VALID_STORY})

    assert response.status_code == 200
    body = response.json()
    assert body["test_cases"][0]["id"] == "TC-001"


def test_generate_test_cases_rejects_short_story():
    response = client.post("/api/generate-test-cases", json={"user_story": "too short"})
    assert response.status_code == 422


def test_generate_test_cases_maps_generator_failure_to_upstream_status():
    fake_generator = MagicMock()
    fake_generator.generate.side_effect = TestCaseGenerationError("upstream failed", status_code=502)
    app.state.generator = fake_generator

    response = client.post("/api/generate-test-cases", json={"user_story": _VALID_STORY})

    assert response.status_code == 502
    assert response.json()["detail"] == "upstream failed"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
