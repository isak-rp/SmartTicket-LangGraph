"""Nodo de limpieza de HTML."""

import re

from src.agents.support.state import TicketState


def clean_html(state: TicketState) -> dict:
    """Elimina etiquetas HTML del contenido crudo entrante."""
    raw_content = state.get("raw_content", "")
    cleaned = re.sub(r"<[^>]*>", "", raw_content)
    return {"content_clean": cleaned}
