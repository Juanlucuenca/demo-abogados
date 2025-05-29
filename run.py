#!/usr/bin/env python3
"""
Script de inicio rápido para el Asistente Legal Inteligente.
Este script facilita el inicio de la aplicación Streamlit.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Verifica que las dependencias estén instaladas"""
    try:
        import streamlit
        import requests
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Falta instalar dependencias: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def check_main_file():
    """Verifica que el archivo principal exista"""
    main_file = Path("core/main.py")
    if main_file.exists():
        print("✅ Archivo principal encontrado")
        return True
    else:
        print("❌ No se encontró core/main.py")
        return False

def check_config():
    """Verifica la configuración de webhooks"""
    try:
        from core.config import get_config
        config = get_config()
        
        # Verificar si están configurados con URLs reales
        upload_configured = config.UPLOAD_WEBHOOK_URL and not config.UPLOAD_WEBHOOK_URL.startswith("https://tu-instancia")
        chat_configured = config.CHAT_WEBHOOK_URL and not config.CHAT_WEBHOOK_URL.startswith("https://tu-instancia")
        
        if upload_configured and chat_configured:
            print("✅ Webhooks configurados correctamente")
        else:
            print("⚠️  Los webhooks usan URLs de ejemplo")
            print("💡 Para funcionalidad completa, configura las URLs reales en core/config.py")
        
        return True
    except Exception as e:
        print(f"❌ Error al verificar configuración: {e}")
        return False

def run_streamlit():
    """Ejecuta la aplicación Streamlit"""
    try:
        print("\n🚀 Iniciando el Asistente Legal Inteligente...")
        print("📱 La aplicación se abrirá en tu navegador automáticamente")
        print("🌐 URL: http://localhost:8501")
        print("⛔ Presiona Ctrl+C para detener la aplicación")
        print("✨ ¡Disfruta de tu asistente legal!\n")
        
        # Ejecutar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "core/main.py",
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 ¡Gracias por usar el Asistente Legal Inteligente!")
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")

def main():
    """Función principal"""
    print("⚖️ Asistente Legal Inteligente - Inicio Rápido")
    print("=" * 55)
    print("🎯 Aplicación plug-and-play para consultas legales inteligentes")
    print()
    
    # Verificar directorio actual
    if not os.path.exists("core"):
        print("❌ Error: Ejecuta este script desde la raíz del proyecto")
        print("💡 Asegúrate de estar en el directorio MVP-abogados")
        sys.exit(1)
    
    # Verificar dependencias
    if not check_requirements():
        sys.exit(1)
    
    # Verificar archivo principal
    if not check_main_file():
        sys.exit(1)
    
    # Verificar configuración
    if not check_config():
        print("⚠️  Continuando con configuración por defecto...")
    
    print("\n🎉 Todo listo para comenzar!")
    
    # Ejecutar aplicación
    run_streamlit()

if __name__ == "__main__":
    main() 