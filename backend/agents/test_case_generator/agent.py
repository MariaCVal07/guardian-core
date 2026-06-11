import json

from backend.llm_client import llm_call


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

        return llm_call(
            system_prompt="Eres un experto en QA Automation.",
            user_prompt=prompt,
            expect_json=False
        )