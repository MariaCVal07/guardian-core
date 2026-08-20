from backend.core.llm_client import llm_call
from backend.core.loaders import load_prompt, load_schema

class AutomationEngine:
    """
    Automation Engine.

    Responsabilidad:
    Determinar la estrategia de automatización de cada
    caso de prueba siguiendo la especificación SDD.
    """

    def evaluate(
        self,
        analysis,
        strategy,
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
        
        # ANÁLISIS FUNCIONAL

        {analysis}

        # ESTRATEGIA DE PRUEBAS

        {strategy}

        # CASOS DE PRUEBA

        {test_design}

        # RESPONDE ÚNICAMENTE EN JSON

        {schema}

        """

        response = llm_call(
            system_prompt="""Eres un QA Automation Architect.

Responde siempre en el mismo idioma del contexto recibido (Business Model, Risk Model, Test Strategy o SDD original). Si el contexto está en español, responde en español. Si está en otro idioma, responde en ese idioma. Nunca traduzcas el contenido recibido. Los nombres de los campos JSON (keys) deben mantenerse siempre en inglés, tal como los define el schema.""",
            user_prompt=prompt,
            expect_json=True
        )

        print("\n===== AUTOMATION ENGINE OUTPUT =====")
        print(response)
        print("====================================\n")

        if response is None:
            return []

        return response.get("automation_decisions", [])