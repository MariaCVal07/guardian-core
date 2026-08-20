from backend.core.llm_client import llm_call
from backend.core.loaders import load_prompt, load_schema

class StrategyEngine:
    """
    Strategy Engine.

    Responsabilidad:
    Construir la estrategia de pruebas utilizando
    la especificación funcional SDD.
    """

    def determine_strategy(
        self,
        business_model,
        risk_model,
    ):

        base_prompt = load_prompt(
            "strategy.md"
        )

        schema = load_schema(
            "strategy.json"
        )

        prompt = f"""
        {base_prompt}

        # BUSINESS MODEL

        {business_model}

        # RISK MODEL

        {risk_model}

        # FORMATO DE RESPUESTA

        {schema}
        """

        response = llm_call(

            system_prompt="""
            Eres el Test Strategy Agent de GUARDIÁN QA.

            Tu única responsabilidad es construir la estrategia de pruebas a partir del Business Model y del Risk Model.

            Debes definir únicamente los objetivos de prueba necesarios para mitigar cada riesgo.

            No vuelvas a interpretar el requerimiento.

            No utilices el SDD.

            No inventes reglas de negocio.

            No inventes riesgos.

            No diseñes casos de prueba.

            No propongas automatización.

            Responde siempre en el mismo idioma del contexto recibido (Business Model, Risk Model, Test Strategy o SDD original). Si el contexto está en español, responde en español. Si está en otro idioma, responde en ese idioma. Nunca traduzcas el contenido recibido. Los nombres de los campos JSON (keys) deben mantenerse siempre en inglés, tal como los define el schema.

            Responde únicamente utilizando el contrato JSON proporcionado.
            """,

            user_prompt=prompt,

            expect_json=True
        )

        print("\n===== STRATEGY ENGINE OUTPUT =====")
        print(response)
        print("==================================\n")

        return response