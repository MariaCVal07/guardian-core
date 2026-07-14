from backend.llm_client import llm_call
from backend.prompt_loader import load_prompt
from backend.schema_loader import load_schema


class StrategyEngine:
    """
    Strategy Engine.

    Responsabilidad:
    Construir la estrategia de pruebas utilizando
    la especificación funcional SDD.
    """

    def determine_strategy(

        self,

        industry,
        product,
        module,
        business_description,
        analysis,

        risk_score
    ):

        base_prompt = load_prompt(
            "strategy.md"
        )

        schema = load_schema(
            "strategy.json"
        )

        prompt = f"""
        {base_prompt}

        # CONTEXTO SDD

        Industria:
        {industry}

        Producto:
        {product}

        Módulo:
        {module}

        Descripción del negocio:
        {business_description}

        # CONTEXTO DEL SDD

        Industria:
        {industry}

        Producto:
        {product}

        Módulo:
        {module}

        Descripción del negocio:
        {business_description}

        # ANÁLISIS FUNCIONAL

        Criticidad:
        {analysis.get("criticality")}

        Impacto:
        {analysis.get("business_impact")}

        Flujos afectados:
        {analysis.get("affected_flows")}

        Riesgos:
        {analysis.get("potential_risks")}

        Mitigaciones:
        {analysis.get("risk_mitigations")}

        # RISK SCORE

        {risk_score}

        # INSTRUCCIONES

        Genera una estrategia de pruebas completa utilizando el contexto del SDD.

        No generes casos de prueba.

        No tomes decisiones de automatización.

        Responde únicamente utilizando el contrato JSON.

        # FORMATO DE RESPUESTA

        {schema}
        """

        response = llm_call(

            system_prompt="Eres un QA Test Architect experto en Risk Based Testing.",

            user_prompt=prompt,

            expect_json=True
        )

        print("\n===== STRATEGY ENGINE OUTPUT =====")
        print(response)
        print("==================================\n")

        return response