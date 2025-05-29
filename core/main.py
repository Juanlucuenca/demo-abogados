import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional
import time
from config import get_config

# Obtener configuración
config = get_config()

# Configuración de la página
st.set_page_config(
    page_title=config.PAGE_TITLE, 
    page_icon=config.PAGE_ICON, 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para una interfaz moderna y limpia
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .section-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .upload-area {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 2px dashed #94a3b8;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    }
    
    .chat-message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        margin-left: 2rem;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .chat-message-assistant {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #334155;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        margin-right: 2rem;
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .success-alert {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border: 1px solid #86efac;
        color: #15803d;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(134, 239, 172, 0.3);
    }
    
    .error-alert {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        border: 1px solid #f87171;
        color: #dc2626;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(248, 113, 113, 0.3);
    }
    
    .info-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #7dd3fc;
        color: #0369a1;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .file-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-section {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Inicializa el estado de la sesión"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "uploaded_files_count" not in st.session_state:
        st.session_state.uploaded_files_count = 0
    if "total_documents" not in st.session_state:
        st.session_state.total_documents = 0

def send_file_to_webhook(file, webhook_url: str) -> tuple[bool, str]:
    """Envía archivo al servicio de procesamiento"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        data = {
            "filename": file.name,
            "upload_time": datetime.now().isoformat(),
            "file_size": len(file.getvalue())
        }
        
        response = requests.post(
            webhook_url,
            files=files,
            data=data,
            timeout=config.WEBHOOK_TIMEOUT_SECONDS
        )
        
        if response.status_code == 200:
            return True, config.MESSAGES["upload_success"].format(filename=file.name)
        else:
            return False, config.MESSAGES["upload_error"].format(error=f"Error del servidor ({response.status_code})")
            
    except requests.exceptions.Timeout:
        return False, config.MESSAGES["timeout_error"]
    except requests.exceptions.ConnectionError:
        return False, config.MESSAGES["connection_error"]
    except Exception as e:
        return False, config.MESSAGES["upload_error"].format(error="Error interno")

def send_message_to_chat_webhook(message: str, webhook_url: str) -> tuple[bool, str]:
    """Envía mensaje al asistente legal"""
    try:
        payload = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "session_id": st.session_state.get("session_id", "user_session")
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=config.WEBHOOK_TIMEOUT_SECONDS
        )
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                print(response_data)
                return True, response_data.get("output", response.text)
            except json.JSONDecodeError:
                return True, response.text
        else:
            return False, config.MESSAGES["chat_error"]
            
    except requests.exceptions.Timeout:
        return False, config.MESSAGES["timeout_error"]
    except requests.exceptions.ConnectionError:
        return False, config.MESSAGES["connection_error"]
    except Exception as e:
        return False, config.MESSAGES["chat_error"]

def render_document_management():
    """Renderiza la sección de gestión de documentos"""
    
    # Título de la sección
    st.markdown("### 📚 Agregar Documentos")
    st.markdown("Sube tus documentos legales para que el asistente pueda ayudarte con consultas específicas.")
    
    # Información sobre tipos de archivo
    st.markdown("""
    **📋 Documentos que puedes subir:**
    - 📄 PDFs (contratos, leyes, reglamentos)
    - 📝 Documentos de Word (.docx)
    """)
    
    # Área de upload
    uploaded_files = st.file_uploader(
        "⬇️ Arrastra tus documentos aquí o haz clic para seleccionar",
        type=config.ALLOWED_FILE_TYPES,
        accept_multiple_files=True,
        help="Selecciona uno o varios documentos para agregar a tu biblioteca legal"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_files:
        st.markdown(f"**📁 Documentos seleccionados: {len(uploaded_files)}**")
        
        # Mostrar archivos seleccionados
        for file in uploaded_files:
            file_size_kb = len(file.getvalue()) / 1024
            st.markdown(f"""
            <div class="file-item">
                <span style="margin-right: 1rem;">📄</span>
                <div style="flex-grow: 1;">
                    <strong>{file.name}</strong><br>
                    <small style="color: #64748b;">{file_size_kb:.1f} KB • {file.type}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Botón para procesar archivos
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Agregar a mi Biblioteca Legal", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                success_count = 0
                error_messages = []
                
                status_text.text(config.MESSAGES["uploading"])
                
                for i, file in enumerate(uploaded_files):
                    progress_bar.progress((i + 1) / len(uploaded_files))
                    
                    success, message = send_file_to_webhook(file, config.UPLOAD_WEBHOOK_URL)
                    
                    if success:
                        success_count += 1
                        st.session_state.uploaded_files_count += 1
                        st.session_state.total_documents += 1
                    else:
                        error_messages.append(f"📄 {file.name}: {message}")
                    
                    time.sleep(0.3)  # Pausa para mejor experiencia visual
                
                progress_bar.empty()
                status_text.empty()
                
                # Mostrar resultados
                if success_count > 0:
                    st.markdown(f'<div class="success-alert">🎉 ¡Perfecto! Se agregaron {success_count} documento(s) a tu biblioteca legal.</div>', unsafe_allow_html=True)
                
                if error_messages:
                    for error in error_messages:
                        st.markdown(f'<div class="error-alert">{error}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_legal_chat():
    """Renderiza la sección de chat legal"""
    
    # Título de la sección
    st.markdown("### 💬 Consulta Legal Inteligente")
    
    # Área de chat
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for role, message, timestamp in st.session_state.chat_history:
                if role == "user":
                    st.markdown(f'''
                    <div class="chat-message-user">
                        <strong>🧑‍💼 Tú • {timestamp}</strong><br><br>
                        {message}
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="chat-message-assistant">
                        <strong>⚖️ Asistente Legal • {timestamp}</strong><br><br>
                        {message}
                    </div>
                    ''', unsafe_allow_html=True)
    
    # Formulario de chat
    st.markdown("---")
    
    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_area(
            "✍️ Escribe tu consulta legal:",
            placeholder="Ejemplo: ¿Cuáles son los pasos para crear una empresa en Colombia?",
            height=120,
            help="Haz preguntas específicas sobre tus documentos legales"
        )
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            submit_button = st.form_submit_button("📤 Enviar Consulta", type="primary", use_container_width=True)
        
        with col2:
            clear_button = st.form_submit_button("🗑️ Limpiar Conversación", use_container_width=True)
        
        with col3:
            st.markdown("")  # Espaciado
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if submit_button and user_message.strip():
        if len(user_message.strip()) < config.MIN_MESSAGE_LENGTH:
            st.markdown(f'<div class="error-alert">{config.MESSAGES["message_too_short"].format(min_length=config.MIN_MESSAGE_LENGTH)}</div>', unsafe_allow_html=True)
            st.stop()
        
        timestamp = datetime.now().strftime("%H:%M")
        
        # Agregar mensaje del usuario
        st.session_state.chat_history.append(("user", user_message, timestamp))
        
        # Procesar consulta
        with st.spinner(config.MESSAGES["processing"]):
            success, response = send_message_to_chat_webhook(user_message, config.CHAT_WEBHOOK_URL)
            
            if success:
                st.session_state.chat_history.append(("assistant", response, timestamp))
            else:
                st.session_state.chat_history.append(("assistant", response, timestamp))
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    initialize_session_state()
    
    # Header principal
    st.markdown(f"""
    <div class="main-header">
        <h1>{config.PAGE_ICON} {config.PAGE_TITLE}</h1>
        <p>Tu asistente personal para consultas legales inteligentes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con información y navegación
    with st.sidebar:
        st.markdown("## 🧭 Secciones")
        page = st.radio(
            "",
            ["📚 Mis Documentos", "💬 Consultas Legales"],
            label_visibility="collapsed"
        )
        
        # Estadísticas
        st.markdown("## 📊 Mi Biblioteca")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📄 Documentos", st.session_state.total_documents)
        
        with col2:
            st.metric("💬 Consultas", len(st.session_state.chat_history))
        
        
        # Guía rápida
        st.markdown("## 🚀 Guía Rápida")
        st.markdown("""
        **1.** 📚 Sube tus documentos legales
        
        **2.** 💬 Haz preguntas específicas
        
        **3.** ⚖️ Recibe respuestas precisas
        
        **4.** 📖 Consulta cuando necesites
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Estado del sistema
        st.markdown("## ⚡ Estado del Sistema")
        st.markdown("🟢 **Conectado y funcionando**")
        st.markdown("🔒 **Tus datos están seguros**")
        st.markdown("🤖 **Asistente listo para ayudar**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Contenido principal
    if page == "📚 Mis Documentos":
        render_document_management()
    elif page == "💬 Consultas Legales":
        render_legal_chat()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.9em; padding: 2rem 0;">
        ⚖️ <strong>Asistente Legal Inteligente</strong> • Consultas precisas basadas en tus documentos • 
        🔒 Información segura y privada
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()





