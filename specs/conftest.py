import os

# backend/core/config.py falla al importarse si no existe GROQ_API_KEY
# (falla rápida intencional para producción). Para poder testear el
# resto del sistema sin depender de una clave real ni de la API de
# Groq, se provee una clave dummy únicamente para la sesión de tests,
# solo si el entorno no ya definió una.
os.environ.setdefault("GROQ_API_KEY", "test-dummy-key")
