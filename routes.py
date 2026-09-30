from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=2000)
    terms: str = Field(..., min_length=2, max_length=8000)
    dates: str = Field(..., min_length=2, max_length=300)
    language: str = Field(default="English", min_length=2, max_length=50)


class DocumentResponse(BaseModel):
    document_type: str
    content: str


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.post("/generate", response_model=DocumentResponse)
def generate_document(payload: DocumentRequest):
    try:
        content = generator.generate_document(
            document_type=payload.document_type,
            parties=payload.parties,
            terms=payload.terms,
            dates=payload.dates,
            language=payload.language,
        )
        return DocumentResponse(document_type=payload.document_type, content=content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {exc}",
        ) from exc
