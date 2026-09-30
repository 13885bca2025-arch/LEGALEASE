# LegalEase — AI-Powered Legal Document Generator

LegalEase is a Streamlit + FastAPI application that generates editable legal-document drafts with Google's Gemini API and exports them as TXT, DOCX, and PDF.

## Project phases

1. Brainstorming & Ideation
2. Requirement Analysis
3. Project Design
4. Project Planning
5. Project Development
6. Project Testing
7. Project Documentation
8. Project Demonstration

## Features

- Legal document draft generation
- Inputs for document type, parties, terms, effective date, and language
- Editable preview
- TXT, DOCX, and PDF downloads
- FastAPI `/generate` endpoint
- Gemini-powered AI generation
- Environment-variable based API-key handling
- Basic automated API/formatter tests

## Folder structure

```text
LegalEase/
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── assets/
├── tests/
│   ├── test_api.py
│   └── test_formatter.py
├── utils/
│   ├── __init__.py
│   └── document_formatter.py
├── .env.example
├── .gitignore
├── app.py
├── main.py
├── requirements.txt
├── routes.py
└── README.md
```

## Setup in VS Code

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and add your Google AI Studio API key:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
LEGALEASE_BACKEND_URL=http://127.0.0.1:8000
```

### 4. Start FastAPI

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to view the API documentation.

### 5. Start Streamlit in a second terminal

```bash
streamlit run app.py
```

Open the URL printed by Streamlit, normally `http://localhost:8501`.

## Test the project

```bash
pytest -q
```

## API example

POST `/generate`

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "ABC Corp (Disclosing Party); Jane Doe (Receiving Party)",
  "terms": "Confidential information must be protected; Disclosure is limited to authorized personnel; Term is 2 years",
  "dates": "September 29, 2026",
  "language": "English"
}
```

## GitHub commands

```bash
git init
git add .
git commit -m "Initial LegalEase project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/LegalEase.git
git push -u origin main
```

## Important API note

The supplied project specification names Gemini 1.5 Pro and the older `google-generativeai` package. Google now recommends the newer `google-genai` SDK. This implementation keeps the documented architecture and functionality while using the current SDK pattern; the model is configurable through `GEMINI_MODEL`.

## Disclaimer

LegalEase produces AI-generated document drafts for educational and productivity purposes. The generated content should be reviewed for the applicable jurisdiction, facts, and intended use before it is signed or relied upon.
