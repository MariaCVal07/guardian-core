import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

CONFIG = {

    # LLM

    "llm_base_url": os.getenv(
        "LLM_BASE_URL",
        "https://api.groq.com/openai/v1"
    ),

    "llm_api_key": os.getenv("GROQ_API_KEY"),

    "llm_model": os.getenv(
        "LLM_MODEL",
        "llama-3.1-8b-instant"
    ),

    "llm_temperature": float(
        os.getenv("LLM_TEMPERATURE", "0.2")
    ),

    # Paths

    "test_output_dir": "playwright/tests/generated",

    "runs_dir": "runs",

    "templates_dir": "frontend/templates",

    # Execution

    "test_runner_cmd": "npx playwright test",

    "test_runner_cwd": "playwright",

    "test_timeout": 60,
}


# Validación crítica al importar

if not CONFIG["llm_api_key"]:
    raise RuntimeError(
        "GROQ_API_KEY no encontrada. "
        "Verifica tu archivo .env"
    )