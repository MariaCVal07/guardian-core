import json
from openai import OpenAI
from backend.core.config import CONFIG
import traceback
import ast

_client = None


def get_client():
    global _client

    if _client is None:
        _client = OpenAI(
            base_url=CONFIG["llm_base_url"],
            api_key=CONFIG["llm_api_key"]
        )

    return _client


def llm_call(system_prompt, user_prompt, expect_json=False, _retry=True):
    """
    Wrapper para llamadas al LLM.

    - Imprime la respuesta completa.
    - Extrae automáticamente el JSON aunque el modelo
      agregue texto o markdown.
    - Reintenta una vez si el JSON falla.
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
            temperature=CONFIG["llm_temperature"],
            max_tokens=5000
        )

        if not response.choices:
            print("[GUARDIAN ERROR] Respuesta vacía del LLM")
            return None

        content = response.choices[0].message.content

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

        # Intentar primero como JSON válido
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            pass

        # Si el modelo devolvió un dict de Python (' en vez de ")
        try:
            return ast.literal_eval(json_text)
        except Exception:
            raise json.JSONDecodeError(
                "La respuesta no es un JSON válido.",
                json_text,
                0
            )

    except json.JSONDecodeError as e:

        print("\n========== JSON INVÁLIDO ==========")
        print(content)
        print("===================================\n")

        print(f"[GUARDIAN ERROR] JSON inválido: {e}")

        if _retry:
            print("[GUARDIAN] Reintentando llamada al LLM...")
            return llm_call(system_prompt, user_prompt, expect_json=expect_json, _retry=False)

        return None

    except Exception as e:

        print("\n========== LLM EXCEPTION ==========")
        traceback.print_exc()
        print("===================================\n")

        return None