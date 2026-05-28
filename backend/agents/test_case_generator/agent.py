import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)


class TestCaseGeneratorAgent:

    def generate_test_case(self, test_data):

        prompt = f"""
        Eres un QA Automation Engineer experto en Playwright y TypeScript.

        Tu objetivo es generar skeletons profesionales de pruebas automatizadas.

        Genera un test Playwright basado en:

        {json.dumps(test_data, indent=2)}

        REGLAS:

        - Usa TypeScript
        - Usa Playwright
        - Genera SOLO UN archivo de test
        - NO repitas código
        - NO generes múltiples versiones
        - NO agregues explicaciones
        - NO agregues markdown
        - NO uses ```typescript
        - SOLO devuelve código limpio
        - El código debe ser ejecutable
        - Usa buenas prácticas QA
        - Usa estructura Arrange / Act / Assert
        - Usa nombres descriptivos
        - El test debe iniciar con:
        import {{ test, expect }} from '@playwright/test';
        """

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto en QA Automation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content
        