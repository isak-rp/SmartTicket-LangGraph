"""Punto de entrada de Streamlit para la demo de clasificación de tickets."""

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from src.agents.support.agent import ticket_agent
from src.api.mock_webhook import get_mock_catalog, get_mock_ticket

load_dotenv()

CATEGORIES = [
    "Fraude y Seguridad",
    "Acceso a la Cuenta",
    "Pagos y Facturación",
    "Gestión de Suscripciones",
    "Solicitud de Reembolsos",
    "Estado de Transacción",
    "Tarjetas Físicas/Digitales",
    "Verificación de Identidad (KYC)",
    "Inversiones y Portafolio",
    "Comisiones y Cargos",
    "Errores de la App/Bug Técnico",
    "Consulta General",
]


def _render_sidebar() -> tuple[dict, str]:
    """Renderiza el selector de mocks y devuelve el ticket seleccionado con el texto editable."""
    st.sidebar.header("Ingesta de Datos")
    st.sidebar.info("Selecciona un escenario mock y ejecuta el flujo completo del agente.")

    catalog = get_mock_catalog()
    mock_keys = list(catalog.keys())

    default_key = mock_keys[0]
    current_key = st.session_state.get("mock_key", default_key)
    if current_key not in catalog:
        current_key = default_key

    selected_key = st.sidebar.selectbox(
        "Tipo de mock",
        options=mock_keys,
        index=mock_keys.index(current_key),
        format_func=lambda key: catalog[key]["label"],
    )

    if st.session_state.get("mock_key") != selected_key:
        st.session_state["mock_key"] = selected_key
        st.session_state["ticket_input"] = get_mock_ticket(selected_key)["raw_content"].strip()

    selected_mock = get_mock_ticket(selected_key)
    st.sidebar.caption(catalog[selected_key]["description"])
    st.sidebar.caption(f"Canal: {selected_mock['source']} | Usuario: {selected_mock['user_id']}")

    if "ticket_input" not in st.session_state:
        st.session_state["ticket_input"] = selected_mock["raw_content"].strip()

    ticket_input = st.sidebar.text_area(
        "Payload del Webhook (Raw)",
        key="ticket_input",
        height=220,
    )
    return selected_mock, ticket_input


def _render_internal_logs(resultado: dict) -> None:
    """Muestra diagnóstico interno, prioridad y texto sanitizado."""
    st.subheader("Análisis Interno")

    llm_error = resultado.get("llm_error", "")
    llm_error_detail = resultado.get("llm_error_detail", "")

    if llm_error == "quota_exceeded":
        st.warning("Gemini sin cuota disponible. Se activó respuesta de respaldo manual.")
    elif llm_error:
        st.warning("Gemini devolvió un error temporal. Se activó respuesta de respaldo manual.")

    if llm_error_detail:
        with st.expander("Ver detalle técnico del error LLM"):
            st.code(llm_error_detail)

    if resultado.get("is_urgent"):
        st.error("Prioridad crítica detectada (posible fraude/robo).")
    else:
        st.success("Prioridad normal.")

    st.text_area(
        "Texto limpio y enmascarado",
        value=resultado.get("content_clean", ""),
        height=170,
        disabled=True,
    )

    confidence = float(resultado.get("confidence", 0))
    st.metric(label="Confianza del modelo", value=f"{confidence * 100:.1f}%")


def _render_agent_output(resultado: dict) -> None:
    """Muestra la categoría y el borrador sugerido en modo editable."""
    st.subheader("Sugerencia para el Agente")

    category_from_model = resultado.get("category", "")
    category_index = CATEGORIES.index(category_from_model) if category_from_model in CATEGORIES else 0

    st.selectbox("Categoría", options=CATEGORIES, index=category_index)
    st.text_area("Borrador", value=resultado.get("draft_response", ""), height=170)

    st.markdown("### Acciones")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if st.button("Aceptar", use_container_width=True):
            st.success("Ticket aceptado y listo para envío.")
    with col_b:
        if st.button("Editar", use_container_width=True):
            st.info("Edición registrada para retroalimentación del sistema.")
    with col_c:
        if st.button("Ignorar", use_container_width=True):
            st.warning("Ticket devuelto a cola manual.")


def main() -> None:
    """Ejecuta la aplicación de Streamlit."""
    st.set_page_config(page_title="AI Support", page_icon="🛡️", layout="wide")
    st.title("Copiloto de Soporte Técnico AI")

    selected_mock, ticket_input = _render_sidebar()

    if not st.sidebar.button("Simular llegada de ticket", type="primary"):
        return

    initial_state = {
        "source": selected_mock["source"],
        "user_id": selected_mock["user_id"],
        "raw_content": ticket_input,
    }

    with st.spinner("Procesando ticket con LangGraph..."):
        try:
            result = ticket_agent.invoke(initial_state)
        except Exception as exc:
            st.error(f"Error procesando el ticket: {exc}")
            st.stop()

    st.divider()
    left_col, right_col = st.columns(2)

    with left_col:
        _render_internal_logs(result)

    with right_col:
        _render_agent_output(result)


if __name__ == "__main__":
    main()
