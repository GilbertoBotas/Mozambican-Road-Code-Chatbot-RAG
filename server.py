import warnings

import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel as PydanticBaseModel
from modules.rag_agent import RAGAgent, RAGAgentResponse

warnings.filterwarnings("ignore", category=UserWarning, message="Pydantic serializer warnings")

app = FastAPI()
agent = RAGAgent()
agent.initialize()

# ── Request / Response schemas ────────────────────────────────────────────────

class AskRequest(PydanticBaseModel):
    question: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "O que é uma contravenção grave?"
            }
        }
    }

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"])
def health():
    """Check if the API is running."""
    return {"status": "ok"}


@app.post("/chat", response_model=RAGAgentResponse)
def ask(request: AskRequest) -> RAGAgentResponse:
    """
    Ask a question. Pass the session_id returned from /session/start.
    Each session maintains its own independent chat history.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        result: RAGAgentResponse = agent.ask(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))