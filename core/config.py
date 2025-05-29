"""
Configuración del MVP del Estudio Jurídico.
Este archivo contiene todas las configuraciones necesarias para el funcionamiento.
"""

import os
from typing import Optional

class Config:
    """Configuración de la aplicación"""
    
    # URLs de webhooks preconfigurados - CAMBIAR ESTAS URLs POR LAS TUYAS
    UPLOAD_WEBHOOK_URL: str = os.getenv("N8N_UPLOAD_WEBHOOK_URL", "https://saludsync.vexy.host/webhook/upload-files")
    CHAT_WEBHOOK_URL: str = os.getenv("N8N_CHAT_WEBHOOK_URL", "https://saludsync.vexy.host/webhook/send-message")
    
    # Configuración de archivos
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_FILE_TYPES: list[str] = ["pdf", "docx", "txt", "md"]
    
    # Configuración de timeouts
    WEBHOOK_TIMEOUT_SECONDS: int = int(os.getenv("WEBHOOK_TIMEOUT_SECONDS", "30"))
    
    # Configuración de la UI
    PAGE_TITLE: str = "Asistente Legal Inteligente"
    PAGE_ICON: str = "⚖️"
    
    # Configuración de validaciones
    MIN_MESSAGE_LENGTH: int = 3
    
    # Mensajes de la aplicación (simplificados y menos técnicos)
    MESSAGES = {
        "upload_success": "✅ Documento '{filename}' agregado exitosamente.",
        "upload_error": "❌ No pudimos procesar el documento: {error}",
        "chat_error": "Lo siento, no pude procesar tu consulta en este momento. Intenta de nuevo.",
        "message_too_short": "❌ Tu consulta es muy corta. Escribe al menos {min_length} caracteres.",
        "no_files_selected": "❌ Por favor selecciona al menos un documento.",
        "processing": "🤔 Analizando tu consulta...",
        "uploading": "📤 Agregando documentos a tu biblioteca...",
        "connection_error": "❌ Problema de conexión. Verifica tu internet e intenta nuevamente.",
        "timeout_error": "⏱️ La consulta está tardando más de lo normal. Intenta nuevamente."
    }

def get_config() -> Config:
    """Retorna la instancia de configuración"""
    return Config()

# INSTRUCCIONES PARA CONFIGURAR TUS WEBHOOKS:
# 
# Opción 1: Cambiar directamente en este archivo
# Modifica las URLs arriba en UPLOAD_WEBHOOK_URL y CHAT_WEBHOOK_URL
#
# Opción 2: Usar variables de entorno (recomendado para producción)
# 
# En Windows (Command Prompt):
# set N8N_UPLOAD_WEBHOOK_URL=https://tu-n8n.app.n8n.cloud/webhook/upload
# set N8N_CHAT_WEBHOOK_URL=https://tu-n8n.app.n8n.cloud/webhook/chat
# 
# En Windows (PowerShell):
# $env:N8N_UPLOAD_WEBHOOK_URL="https://tu-n8n.app.n8n.cloud/webhook/upload"
# $env:N8N_CHAT_WEBHOOK_URL="https://tu-n8n.app.n8n.cloud/webhook/chat"
#
# En Linux/Mac:
# export N8N_UPLOAD_WEBHOOK_URL=https://tu-n8n.app.n8n.cloud/webhook/upload
# export N8N_CHAT_WEBHOOK_URL=https://tu-n8n.app.n8n.cloud/webhook/chat 