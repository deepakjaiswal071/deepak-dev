from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings
from app.services.openai_client import OpenAIClient
from app.services.test_case_generator import TestCaseGenerationService

app = FastAPI(title="AI Test Case Generator")

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origin],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.state.generator = TestCaseGenerationService(OpenAIClient(settings))

app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
