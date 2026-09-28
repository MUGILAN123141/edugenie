# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied project documentation.

## Features

- Q&A — `POST /qa`
- Simple concept explanation — `POST /explain`
- Four-option quiz generation — `POST /quiz`
- Passage summarization — `POST /summarize`
- Personalized learning path — `POST /learn/recommendations`
- Health check — `GET /health`
- Responsive browser UI at `/`

The supplied documentation describes Gemini 1.5 Pro for Q&A, summarization, quizzes and learning paths, and LaMini-Flan-T5-783M for explanations. The implementation keeps those roles but makes the Gemini model configurable because model availability changes over time.

## 1. Prerequisites

- Python 3.10+
- VS Code
- A Gemini API key from Google AI Studio

## 2. Create a virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For the optional local LaMini-Flan-T5 explanation model:

```bash
pip install -r requirements-local.txt
```

## 4. Configure the API key

Copy `.env.example` to `.env` and put your Gemini API key in `GEMINI_API_KEY`.

Do not commit `.env`.

## 5. Run

```bash
uvicorn main:app --reload
```

Open:

`http://127.0.0.1:8000`

Interactive API docs:

`http://127.0.0.1:8000/docs`

## 6. Test

Run:

```bash
pytest -q
```

Manual health check:

```bash
curl http://127.0.0.1:8000/health
```

Q&A:

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"Which is the largest ocean?\"}"
```

On macOS/Linux use `\` instead of `^` for multiline commands.

## Architecture

```text
EduGenie/
├── main.py
├── config.py
├── schemas.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    ├── test_api.py
    └── test_modules.py
```

## Notes

The API key is read only from the environment. Gemini calls happen server-side, so the key is never exposed to browser JavaScript.

The local model is lazy-loaded only when `ENABLE_LOCAL_EXPLANATION=true`. This avoids downloading a large model during a normal first installation.

The quiz endpoint uses Gemini structured JSON output plus Pydantic validation, rather than depending on fragile Markdown-code-block cleanup.
