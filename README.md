# ⚖️ Asistente Legal Inteligente

Una aplicación moderna y fácil de usar que permite a estudios de abogados y profesionales legales gestionar documentos y hacer consultas inteligentes usando un asistente virtual.

## 🚀 Características Principales

- **📚 Biblioteca Legal Personal**: Sube documentos PDF, DOCX, TXT y MD
- **💬 Consultas Inteligentes**: Chatea con tus documentos para obtener respuestas precisas
- **🎨 Interfaz Moderna**: Diseño limpio y profesional
- **⚡ Plug & Play**: Sin configuración técnica - funciona inmediatamente
- **🔒 Seguro y Privado**: Tus documentos permanecen seguros

## 📋 Requisitos

- Python 3.8 o superior
- Conexión a internet
- Instancia de N8N configurada (para desarrolladores)

## 🛠️ Instalación Rápida

1. **Descarga el proyecto**
```bash
git clone <tu-repositorio>
cd MVP-abogados
```

2. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

3. **Configura tus webhooks** (solo si eres el desarrollador)
   - Edita `core/config.py`
   - Cambia las URLs de `UPLOAD_WEBHOOK_URL` y `CHAT_WEBHOOK_URL`

4. **¡Listo para usar!**
```bash
python run.py
```

## 🎯 Uso de la Aplicación

### Para Usuarios Finales

La aplicación está diseñada para ser extremadamente fácil de usar:

#### 1. 📚 Agregar Documentos
- Abre la sección "Mis Documentos"
- Arrastra tus archivos legales o haz clic para seleccionar
- Presiona "Agregar a mi Biblioteca Legal"
- ¡Listo! Tus documentos están disponibles para consultas

#### 2. 💬 Hacer Consultas
- Ve a "Consultas Legales"
- Escribe tu pregunta en lenguaje natural
- Recibe respuestas basadas en tus documentos
- Mantén conversaciones fluidas con el asistente

### Ejemplos de Preguntas

- "¿Cuáles son los requisitos para constituir una sociedad?"
- "¿Qué documentos necesito para un contrato de trabajo?"
- "Explícame los pasos para registrar una marca"
- "¿Cuáles son las obligaciones fiscales de una empresa?"

## 🎨 Características de la Interfaz

### Diseño Intuitivo
- **Navegación simple**: Solo dos secciones principales
- **Arrastrar y soltar**: Sube documentos fácilmente
- **Chat natural**: Conversa como si fuera WhatsApp
- **Progreso visual**: Ve el estado de tus uploads

### Información en Tiempo Real
- **Contador de documentos**: Ve cuántos archivos has subido
- **Historial de chat**: Mantiene tus conversaciones
- **Estado del sistema**: Indicadores de conexión
- **Guía rápida**: Ayuda siempre visible

## 🔧 Para Desarrolladores

### Configuración de Webhooks

La aplicación usa dos webhooks de N8N:

1. **Webhook de Upload** (`UPLOAD_WEBHOOK_URL`)
   - Recibe documentos y los procesa
   - Estructura esperada: multipart/form-data
   - Debe responder con status 200 para éxito

2. **Webhook de Chat** (`CHAT_WEBHOOK_URL`)
   - Recibe consultas y devuelve respuestas
   - Formato JSON con campo "message"
   - Debe responder con JSON: `{"response": "respuesta"}`

### Configuración Rápida

**Opción 1: Editar directamente el archivo**
```python
# En core/config.py
UPLOAD_WEBHOOK_URL = "https://tu-n8n.app.n8n.cloud/webhook/upload"
CHAT_WEBHOOK_URL = "https://tu-n8n.app.n8n.cloud/webhook/chat"
```

**Opción 2: Variables de entorno**
```bash
# Windows PowerShell
$env:N8N_UPLOAD_WEBHOOK_URL="https://tu-n8n.app.n8n.cloud/webhook/upload"
$env:N8N_CHAT_WEBHOOK_URL="https://tu-n8n.app.n8n.cloud/webhook/chat"

# Linux/Mac
export N8N_UPLOAD_WEBHOOK_URL=https://tu-n8n.app.n8n.cloud/webhook/upload
export N8N_CHAT_WEBHOOK_URL=https://tu-n8n.app.n8n.cloud/webhook/chat
```

### Estructura de Datos

**Upload Request:**
```json
{
  "filename": "contrato.pdf",
  "upload_time": "2024-01-20T10:30:00",
  "file_size": 1024000
}
```

**Chat Request:**
```json
{
  "message": "¿Cómo registro una empresa?",
  "timestamp": "2024-01-20T10:30:00",
  "session_id": "user_session"
}
```

**Chat Response:**
```json
{
  "response": "Para registrar una empresa necesitas..."
}
```

## 🎨 Personalización

### Cambiar Colores
Edita los gradientes CSS en `core/main.py`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Agregar Tipos de Archivo
En `core/config.py`:
```python
ALLOWED_FILE_TYPES = ["pdf", "docx", "txt", "md", "xlsx"]
```

### Modificar Mensajes
Cambia los textos en `core/config.py`:
```python
MESSAGES = {
    "upload_success": "Tu mensaje personalizado",
    ...
}
```

## 🚀 Despliegue

### Local
```bash
python run.py
```

### Servidor
```bash
streamlit run core/main.py --server.port 8501 --server.address 0.0.0.0
```

### Docker (opcional)
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "core/main.py"]
```

## 🐛 Solución de Problemas

### La aplicación no inicia
```bash
# Verifica Python
python --version

# Reinstala dependencias
pip install --upgrade -r requirements.txt
```

### Los documentos no se suben
1. Verifica tu conexión a internet
2. Comprueba que las URLs de N8N estén correctas
3. Revisa los logs de N8N

### El chat no responde
1. Verifica la configuración del webhook de chat
2. Comprueba que N8N esté funcionando
3. Revisa el formato de respuesta JSON

## 📊 Límites y Especificaciones

- **Tamaño máximo de archivo**: 10 MB por defecto
- **Tipos soportados**: PDF, DOCX, TXT, MD
- **Timeout de webhooks**: 30 segundos
- **Sesiones**: Persistentes durante la sesión del navegador

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b nueva-funcionalidad`
3. Haz commit: `git commit -am 'Agregar funcionalidad'`
4. Push: `git push origin nueva-funcionalidad`
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

---

**🚀 ¡Listo para usar! Sin configuración técnica requerida para usuarios finales.** # demo-abogados
