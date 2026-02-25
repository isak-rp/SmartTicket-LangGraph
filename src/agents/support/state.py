"""Estado compartido que fluye entre los nodos de LangGraph."""

from typing import TypedDict


class TicketState(TypedDict, total=False):
    source: str
    user_id: str
    raw_content: str
    is_urgent: bool
    content_clean: str
    category: str
    confidence: float
    draft_response: str
    llm_error: str
    llm_error_detail: str
