from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    QARequest, ExplainRequest, QuizRequest, SummaryRequest,
    LearningPathRequest, APIResponse
)
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import recommend_learning_path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa", response_model=APIResponse)
async def qa(payload: QARequest):
    return APIResponse(success=True, data={"answer": answer_question(payload.question)})


@app.post("/explain", response_model=APIResponse)
async def explain(payload: ExplainRequest):
    return APIResponse(success=True, data={"explanation": explain_topic(payload.topic, payload.level)})


@app.post("/quiz", response_model=APIResponse)
async def quiz(payload: QuizRequest):
    return APIResponse(success=True, data={"quiz": generate_quiz(payload.topic, payload.count, payload.level)})


@app.post("/summarize", response_model=APIResponse)
async def summarize(payload: SummaryRequest):
    return APIResponse(success=True, data={"summary": summarize_text(payload.text, payload.level)})


@app.post("/learn/recommendations", response_model=APIResponse)
async def recommendations(payload: LearningPathRequest):
    return APIResponse(
        success=True,
        data={"recommendations": recommend_learning_path(payload.topic, payload.level, payload.goal)}
    )
