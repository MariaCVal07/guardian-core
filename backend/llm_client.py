import json
from openai import OpenAI
from backend.config import CONFIG
import traceback

_client = None


def get_client():
    global _client

    if _client is None:
        _client = OpenAI(
            base_url=CONFIG["llm_base_url"],
            api_key=CONFIG["llm_api_key"]
        )

    return _client


def llm_call(system_prompt, user_prompt, expect_json=False):
    """
    Wrapper para llamadas al LLM.

    - Imprime la respuesta completa.
    - Extrae automáticamente el JSON aunque el modelo
      agregue texto o markdown.
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

        print("\n========== RAW LLM RESPONSE ==========")
        print(content)
        print("======================================\n")

        if not expect_json:
            return content

        # -----------------------------
        # Limpieza automática
        # -----------------------------

        content = content.strip()

        # Elimina ```json ... ```
        if "```" in content:
            content = (
                content
                .replace("```json", "")
                .replace("```JSON", "")
                .replace("```", "")
                .strip()
            )

        # Busca el primer objeto JSON
        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            raise json.JSONDecodeError(
                "No se encontró un objeto JSON.",
                content,
                0
            )

        json_text = content[start:end + 1]

        return json.loads(json_text)

    except json.JSONDecodeError as e:

        print("\n========== JSON INVÁLIDO ==========")
        print(content)
        print("===================================\n")

        print(f"[GUARDIAN ERROR] JSON inválido: {e}")

        return None

    except Exception as e:

        print("\n========== LLM EXCEPTION ==========")
        traceback.print_exc()
        print("===================================\n")

        return None