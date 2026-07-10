from typing import Literal

from pydantic import BaseModel, Field, field_validator

TestCaseType = Literal["Positive", "Negative", "Boundary"]


class TestCase(BaseModel):
    id: str
    scenario: str
    preconditions: str
    steps: list[str]
    expected_result: str
    type: TestCaseType


class TestCaseCollection(BaseModel):
    test_cases: list[TestCase]


class GenerateRequest(BaseModel):
    user_story: str = Field(min_length=20, max_length=6000)

    @field_validator("user_story")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("user_story must not be blank")
        return value
