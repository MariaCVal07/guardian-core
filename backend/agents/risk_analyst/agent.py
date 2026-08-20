from backend.core.llm_client import llm_call
from backend.core.loaders import load_prompt, load_schema


class RiskAnalystAgent:
    """
    Risk Analyst Agent.

    Responsabilidad:

    Identificar riesgos funcionales a partir del modelo del dominio
    generado por el Business Analyst y definir las mitigaciones
    orientadas a QA.

    Especificación funcional:

    risk_analyst.md

    Contrato de salida:

    risk_analyst.json
    """

    def analyze_risks(
        self,
        analysis
    ):

        base_prompt = load_prompt(
            "risk_analyst.md"
        )

        schema = load_schema(
            "risk_analyst.json"
        )

        prompt = f"""
        {base_prompt}

        # BUSINESS MODEL (ÚNICA FUENTE DE VERDAD)

        El siguiente JSON fue generado y validado por el Business Analyst.

        Utiliza exclusivamente esta información.

        No reconstruyas el requerimiento.

        No agregues información que no exista en este modelo.

        {analysis}

        # FORMATO DE RESPUESTA

        {schema}
        """

        response = llm_call(
            system_prompt="""
            Eres el Functional Risk Analyst de GUARDIÁN QA.

            Tu única entrada es el Business Model generado por el Business Analyst.

            Ese modelo es la única fuente de verdad.

            Nunca vuelvas a interpretar el requerimiento original.

            Nunca utilices conocimiento del dominio.

            Cada riesgo debe derivarse de exactamente un elemento del Business Model.

            Si el Business Model no contiene una regla, restricción, invariante o estado inválido, no puedes generar un riesgo.

            No combines varias reglas en un mismo riesgo.

            No generes riesgos adicionales.

            No inventes entidades.

            No inventes funcionalidades.

            No generes casos de prueba.

            No generes estrategias.

            Responde siempre en el mismo idioma del contexto recibido (Business Model, Risk Model, Test Strategy o SDD original). Si el contexto está en español, responde en español. Si está en otro idioma, responde en ese idioma. Nunca traduzcas el contenido recibido. Los nombres de los campos JSON (keys) deben mantenerse siempre en inglés, tal como los define el schema.

            Responde únicamente utilizando el JSON solicitado.
            """,

            user_prompt=prompt,
            expect_json=True
        )

        print("\n===== RISK ANALYST OUTPUT =====")
        print(response)
        print("================================\n")

        return response