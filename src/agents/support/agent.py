"""Definición del flujo de LangGraph para el procesamiento de tickets de soporte."""

from langgraph.graph import END, START, StateGraph

from src.agents.support.nodes.limpiador.node import clean_html
from src.agents.support.nodes.llm_gemini.node import classify_with_gemini
from src.agents.support.nodes.mascara.node import mask_pii_data
from src.agents.support.nodes.priorizador.node import prioritize_ticket
from src.agents.support.state import TicketState


def build_ticket_agent():
    """Construye y compila el flujo de procesamiento de tickets."""
    workflow = StateGraph(TicketState)

    workflow.add_node("clean_html", clean_html)
    workflow.add_node("prioritize_ticket", prioritize_ticket)
    workflow.add_node("mask_pii_data", mask_pii_data)
    workflow.add_node("classify_with_gemini", classify_with_gemini)

    workflow.add_edge(START, "clean_html")
    workflow.add_edge("clean_html", "prioritize_ticket")
    workflow.add_edge("prioritize_ticket", "mask_pii_data")
    workflow.add_edge("mask_pii_data", "classify_with_gemini")
    workflow.add_edge("classify_with_gemini", END)

    return workflow.compile()


ticket_agent = build_ticket_agent()
