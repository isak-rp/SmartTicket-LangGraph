"""Nodo de clasificación con Gemini, salida estructurada y fallback robusto."""

import os

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from src.agents.support.nodes.llm_gemini.prompt import PROMPT_TEMPLATE
from src.agents.support.state import TicketState


class ClasificacionTicket(BaseModel):
    """Contrato de salida estructurada para el modelo clasificador."""

    category: str = Field(description="Debe ser exactamente una de las 12 categorías permitidas.")
    confidence: float = Field(description="Nivel de confianza entre 0.0 y 1.0.")
    draft_response: str = Field(description="Borrador de respuesta para el cliente.")


def classify_with_gemini(state: TicketState) -> dict:
    """Clasifica el ticket enmascarado y aplica fallback si el modelo falla."""
    model_name = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
    structured_llm = llm.with_structured_output(ClasificacionTicket)

    safe_text = state.get("content_clean", "")
    prompt = PROMPT_TEMPLATE.format(ticket_text=safe_text)

    try:
        result = structured_llm.invoke(prompt)
        return {
            "category": result.category,
            "confidence": result.confidence,
            "draft_response": result.draft_response,
            "llm_error": "",
            "llm_error_detail": "",
        }
    except Exception as exc:
        error_msg = str(exc)
        normalized_error = error_msg.lower()
        is_quota_error = "resource_exhausted" in normalized_error or "quota" in normalized_error

        if is_quota_error:
            return {
                "category": "Consulta General",
                "confidence": 0.0,
                "draft_response": (
                    "No pude generar respuesta automática por límite de cuota del modelo. "
                    "Por favor, responder manualmente este ticket."
                ),
                "llm_error": "quota_exceeded",
                "llm_error_detail": error_msg,
            }

        return {
            "category": "Consulta General",
            "confidence": 0.0,
            "draft_response": (
                "No pude generar respuesta automática por un error temporal del modelo. "
                "Por favor, responder manualmente este ticket."
            ),
            "llm_error": "model_error",
            "llm_error_detail": error_msg,
        }
