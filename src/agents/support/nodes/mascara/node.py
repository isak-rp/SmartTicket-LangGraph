"""Nodo de enmascaramiento de datos sensibles (PII)."""

import re

from src.agents.support.state import TicketState


EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
CARD_PATTERN = r"\\b(?:\\d[ -]*?){13,16}\\b"
PHONE_PATTERN = r"\\+?\\d{10,13}"


def mask_pii_data(state: TicketState) -> dict:
    """Enmascara correos, tarjetas y teléfonos dentro del contenido."""
    text = state.get("content_clean", "")
    masked = re.sub(EMAIL_PATTERN, "[CORREO_OCULTO]", text)
    masked = re.sub(CARD_PATTERN, "[TARJETA_OCULTA]", masked)
    masked = re.sub(PHONE_PATTERN, "[TELEFONO_OCULTO]", masked)
    return {"content_clean": masked}
