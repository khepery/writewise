"""
FastAPI REST API for WriteWise grammar checker.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

from contextlib import asynccontextmanager

from writewise.core.grammar_checker import GrammarChecker, AnalysisResult


# Pydantic models for API
class CheckRequest(BaseModel):
    """Request model for grammar checking."""
    text: str = Field(..., description="Text to check for grammar issues")
    auto_correct: bool = Field(False, description="Whether to return auto-corrected text")


class GrammarIssueResponse(BaseModel):
    """Response model for a grammar issue."""
    message: str
    rule_id: str
    category: str
    offset: int
    length: int
    context: str
    suggestions: List[str]
    severity: str


class StyleSuggestionResponse(BaseModel):
    """Response model for a style suggestion."""
    message: str
    category: str
    offset: int
    length: int
    original: str
    suggestion: str


class ReadabilityResponse(BaseModel):
    """Response model for readability metrics."""
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    gunning_fog: float
    smog_index: float
    automated_readability_index: float
    coleman_liau_index: float
    difficult_words: int
    reading_time_minutes: float


class CheckResponse(BaseModel):
    """Response model for grammar checking."""
    original_text: str
    corrected_text: Optional[str] = None
    grammar_issues: List[GrammarIssueResponse]
    style_suggestions: List[StyleSuggestionResponse]
    readability: ReadabilityResponse
    word_count: int
    sentence_count: int
    character_count: int
    score: float


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


# Global checker instance
checker = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    global checker
    # Startup
    checker = GrammarChecker(use_language_tool=False)
    yield
    # Shutdown
    if checker:
        checker.close()


# Create FastAPI app
app = FastAPI(
    title="WriteWise Grammar Checker API",
    description="Advanced grammar checking API for students, teachers, and writers",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return HealthResponse(status="ok", version="1.0.0")


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(status="ok", version="1.0.0")


@app.post("/api/check", response_model=CheckResponse)
async def check_grammar(request: CheckRequest):
    """
    Check text for grammar, style, and readability issues.
    
    Args:
        request: CheckRequest containing text to analyze
        
    Returns:
        CheckResponse with all issues and metrics
    """
    global checker
    
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Initialize checker if not already done (for testing)
        if checker is None:
            checker = GrammarChecker(use_language_tool=False)
        
        # Analyze text
        result = checker.analyze(request.text)
        
        # Convert to response models
        grammar_issues = [
            GrammarIssueResponse(
                message=issue.message,
                rule_id=issue.rule_id,
                category=issue.category,
                offset=issue.offset,
                length=issue.length,
                context=issue.context,
                suggestions=issue.suggestions,
                severity=issue.severity
            )
            for issue in result.grammar_issues
        ]
        
        style_suggestions = [
            StyleSuggestionResponse(
                message=sug.message,
                category=sug.category,
                offset=sug.offset,
                length=sug.length,
                original=sug.original,
                suggestion=sug.suggestion
            )
            for sug in result.style_suggestions
        ]
        
        readability = ReadabilityResponse(
            flesch_reading_ease=result.readability.flesch_reading_ease,
            flesch_kincaid_grade=result.readability.flesch_kincaid_grade,
            gunning_fog=result.readability.gunning_fog,
            smog_index=result.readability.smog_index,
            automated_readability_index=result.readability.automated_readability_index,
            coleman_liau_index=result.readability.coleman_liau_index,
            difficult_words=result.readability.difficult_words,
            reading_time_minutes=result.readability.reading_time_minutes
        )
        
        # Auto-correct if requested
        corrected_text = None
        if request.auto_correct:
            corrected_text = checker.correct_text(request.text)
        
        return CheckResponse(
            original_text=result.original_text,
            corrected_text=corrected_text,
            grammar_issues=grammar_issues,
            style_suggestions=style_suggestions,
            readability=readability,
            word_count=result.word_count,
            sentence_count=result.sentence_count,
            character_count=result.character_count,
            score=result.score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the API server."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
