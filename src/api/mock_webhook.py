"""Payloads mock para simular tickets entrantes desde distintos canales."""

from __future__ import annotations

from typing import Dict, TypedDict


class MockTicket(TypedDict):
    label: str
    description: str
    source: str
    user_id: str
    raw_content: str


MOCK_TICKETS: Dict[str, MockTicket] = {
    "email_fraude_urgente": {
        "label": "Email: Fraude urgente",
        "description": "Caso crítico con posible acceso no autorizado y cargo desconocido.",
        "source": "email",
        "user_id": "usr_998877",
        "raw_content": """
<html><body>
<p>¡AYUDA URGENTE! Me robaron el celular en el metro y creo que entraron a mi app.
Hay un cargo de $5000 que yo no hice. Mi correo es isaac.ramirez@gmail.com y mi cel
es +525551234567. ¡Bloqueen mi cuenta por favor!</p>
</body></html>
""",
    },
    "chat_doble_cobro": {
        "label": "Chat: Doble cobro",
        "description": "Ticket cotidiano de facturación con tono neutral.",
        "source": "chat",
        "user_id": "usr_145220",
        "raw_content": "Hola equipo, este mes me cobraron dos veces el plan premium. ¿Me ayudan a revisar?",
    },
    "whatsapp_cancelacion": {
        "label": "WhatsApp: Cancelación de suscripción",
        "description": "Solicitud habitual para cancelar un plan y evitar renovaciones.",
        "source": "whatsapp",
        "user_id": "usr_778901",
        "raw_content": "Buenas, quiero cancelar mi suscripción anual desde hoy. No quiero más renovaciones automáticas.",
    },
    "chat_error_app_diffuso": {
        "label": "Chat: Bug difuso en la app",
        "description": "Caso ambiguo con comportamiento inestable sin error explícito.",
        "source": "chat",
        "user_id": "usr_556612",
        "raw_content": "Desde ayer la app se traba a veces cuando abro movimientos. No siempre pasa y no sale mensaje de error.",
    },
    "email_consulta_cotidiana": {
        "label": "Email: Consulta cotidiana",
        "description": "Pregunta general sobre comisiones y funcionamiento normal de cuenta.",
        "source": "email",
        "user_id": "usr_112233",
        "raw_content": "Hola, ¿me pueden confirmar si la transferencia SPEI tiene comisión en su plan básico? Gracias.",
    },
}


def get_mock_catalog() -> Dict[str, MockTicket]:
    """Devuelve el catálogo completo de tickets mock disponibles."""
    return MOCK_TICKETS


def get_mock_ticket(mock_key: str = "email_fraude_urgente") -> MockTicket:
    """Devuelve un ticket mock por clave y usa el predeterminado si la clave no existe."""
    return MOCK_TICKETS.get(mock_key, MOCK_TICKETS["email_fraude_urgente"])
