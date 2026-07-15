from backend.llm_client import llm_call
from backend.prompt_loader import load_prompt
from backend.schema_loader import load_schema


class TestDesignerAgent:

    def generate_tests(
        self,
        analysis,
        requirement,
        acceptance_criteria
    ):

        base_prompt = load_prompt(
            "test_design.md"
        )

        schema = load_schema(
            "test_design.json"
        )

        prompt = f"""
        {base_prompt}

        # CONTEXTO

        # ANÁLISIS FUNCIONAL

        {analysis}

        # REQUERIMIENTO

        {requirement}

        # CRITERIOS DE ACEPTACIÓN

        {acceptance_criteria}
        
        # RESPONDE ÚNICAMENTE EN JSON

        NO escribas explicaciones.

        NO escribas texto adicional.

        NO uses Markdown.

        NO uses ```json.

        Devuelve EXACTAMENTE un objeto JSON con esta estructura:

        {schema}
        """

        response = llm_call(
            system_prompt="Eres un QA Senior experto en Test Design.",
            user_prompt=prompt,
            expect_json=True
        )

        if response is None:
           return []

        print("\n===== TEST DESIGNER OUTPUT =====")
        print(response)
        print("================================\n")

        return response.get("tests", [])