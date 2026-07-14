from backend.llm_client import llm_call
from backend.prompt_loader import load_prompt
from backend.schema_loader import load_schema


class AutomationEngine:
    """
    Automation Engine.

    Responsabilidad:
    Determinar la estrategia de automatización de cada
    caso de prueba siguiendo la especificación SDD.
    """

    def evaluate(
        self,
        test_design
    ):

        base_prompt = load_prompt(
            "automation.md"
        )

        schema = load_schema(
            "automation.json"
        )

        prompt = f"""
        {base_prompt}

        # CASOS DE PRUEBA

        {test_design}

        # FORMATO DE RESPUESTA

        {schema}
        """

        response = llm_call(
            system_prompt="Eres un QA Automation Architect.",
            user_prompt=prompt,
            expect_json=True
        )

        print("\n===== AUTOMATION ENGINE OUTPUT =====")
        print(response)
        print("====================================\n")

        if response is None:
            return []

        return response.get("automation_decisions", [])