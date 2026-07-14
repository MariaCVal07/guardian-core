from backend.llm_client import llm_call
from backend.prompt_loader import load_prompt
from backend.schema_loader import load_schema


class RiskAnalystAgent:
    """
    Risk Analyst Agent.

    Responsabilidad:
    Analizar los riesgos identificados y proponer
    recomendaciones de mitigación orientadas a QA.

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

# ANÁLISIS FUNCIONAL

{analysis}

# FORMATO DE RESPUESTA

{schema}
"""

        response = llm_call(
            system_prompt="Eres un QA Senior experto en Risk Based Testing.",
            user_prompt=prompt,
            expect_json=True
        )

        print("\n===== RISK ANALYST OUTPUT =====")
        print(response)
        print("================================\n")

        return response