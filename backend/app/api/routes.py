from fastapi import APIRouter, HTTPException, Request

from app.models import GenerateRequest, TestCaseCollection
from app.services.test_case_generator import TestCaseGenerationError

router = APIRouter()


@router.post("/api/generate-test-cases", response_model=TestCaseCollection)
def generate_test_cases(payload: GenerateRequest, request: Request) -> TestCaseCollection:
    generator = request.app.state.generator
    try:
        return generator.generate(payload.user_story)
    except TestCaseGenerationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
