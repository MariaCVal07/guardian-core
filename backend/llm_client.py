import json
# pyrefly: ignore [missing-import]
from openai import OpenAI
from backend.config import CONFIG


_client = None


def get_client():
    """Crea el cliente OpenAI una sola vez (lazy init)."""

    global _client

    if _client is None:

        _client = OpenAI(
            base_url=CONFIG["llm_base_url"],
            api_key=CONFIG["llm_api_key"]
        )

    return _client


def llm_call(system_prompt, user_prompt, expect_json=False):
    """Llama al LLM con manejo de errores.

    Args:
        system_prompt: Rol del sistema.
        user_prompt: Prompt del usuario.
        expect_json: Si True, parsea la respuesta como JSON.

    Returns:
        str o dict según expect_json.
        None si hay error.
    """

    client = get_client()

    try:

        response = client.chat.completions.create(

            model=CONFIG["llm_model"],

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=CONFIG["llm_temperature"]
        )

        if not response.choices:
            print("[GUARDIAN ERROR] Respuesta vacía del LLM")
            return None

        content = response.choices[0].message.content

        if expect_json:

            content = content.strip()

            # Limpiar markdown wrapping si el LLM lo agrega
            if content.startswith("```"):
                content = content.split("\n", 1)[1]
                content = content.rsplit("```", 1)[0]

            return json.loads(content)

        return content

    except json.JSONDecodeError as e:

        print(f"[GUARDIAN ERROR] LLM devolvió respuesta no-JSON: {e}")
        return None

    except Exception as e:

        print(f"[GUARDIAN ERROR] Fallo en llamada LLM: {e}")
        return None
