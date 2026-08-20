from backend.core.llm_client import llm_call
from backend.core.loaders import load_prompt, load_schema


class TestDesignerAgent:

    def generate_tests(
        self,
        business_model,
        risk_model,
        strategy
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

        # BUSINESS MODEL

        {business_model}

        # RISK MODEL

        {risk_model}

        # TEST STRATEGY

        {strategy}
        
        # RESPONDE ÚNICAMENTE EN JSON

        NO escribas explicaciones.

        NO escribas texto adicional.

        NO uses Markdown.

        NO uses ```json.

        Devuelve EXACTAMENTE un objeto JSON con esta estructura:

        {schema}
        """

        response = llm_call(
            system_prompt= """
            Eres el Test Designer Agent de GUARDIÁN QA.

            Tu única responsabilidad es diseñar los casos de prueba a partir del Business Model, el Risk Model y la Test Strategy.

            No vuelvas a interpretar el requerimiento.
            No utilices el SDD.
            No inventes reglas de negocio.
            No inventes riesgos.
            Responde siempre en el mismo idioma del contexto recibido (Business Model, Risk Model, Test Strategy o SDD original). Si el contexto está en español, responde en español. Si está en otro idioma, responde en ese idioma. Nunca traduzcas el contenido recibido. Los nombres de los campos JSON (keys) deben mantenerse siempre en inglés, tal como los define el schema.

            Responde únicamente con el JSON solicitado.
            """,
            
            user_prompt=prompt,
            expect_json=True
        )

        if response is None:
           return []

        print("\n===== TEST DESIGNER OUTPUT =====")
        print(response)
        print("================================\n")

        return response.get("tests", [])