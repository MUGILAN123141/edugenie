from pydantic import BaseModel, Field, field_validator

class QARequest(BaseModel):
    question: str = Field(min_length=2, max_length=20000)

class ExplainRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=10000)
    level: str = Field(default="beginner", max_length=50)

class QuizRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=10000)
    count: int = Field(default=5, ge=1, le=20)
    level: str = Field(default="beginner", max_length=50)

class SummaryRequest(BaseModel):
    text: str = Field(min_length=20, max_length=50000)
    level: str = Field(default="beginner", max_length=50)

class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=10000)
    level: str = Field(default="beginner", max_length=50)
    goal: str = Field(default="understand the topic well", max_length=1000)

class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str

class QuizResult(BaseModel):
    topic: str
    questions: list[QuizQuestion]

class APIResponse(BaseModel):
    success: bool
    data: dict
