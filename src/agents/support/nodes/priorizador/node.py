"""Nodo de detección de urgencia."""

from src.agents.support.state import TicketState


URGENT_KEYWORDS = [
    "es un fraude",
    "cancelacion",
    "ya no quiero esto",
    "robaron",
    "cargo que yo no hice",
    "no reconozco este cargo",
    "bloqueen mi cuenta",
]


def prioritize_ticket(state: TicketState) -> dict:
    """Marca el ticket como urgente cuando detecta patrones de riesgo de fraude."""
    text = state.get("content_clean", "").lower()
    is_urgent = any(keyword in text for keyword in URGENT_KEYWORDS)
    return {"is_urgent": is_urgent}
