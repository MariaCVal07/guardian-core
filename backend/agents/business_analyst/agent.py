from backend.llm_client import llm_call
from backend.prompt_loader import load_prompt
from backend.schema_loader import load_schema

class BusinessAnalystAgent:

    def analyze_requirement(

        self,

        industry,

        product,

        module,

        business_description,

        requirement,

        acceptance_criteria
    ):

        base_prompt = load_prompt(
            __file__,
            "business_analyst.md"
        )

        schema = load_schema(
            __file__,
            "business_analyst.json"
        )  

        prompt = f"""
        {base_prompt}

        # CONTEXTO DEL SDD

        Industria:
        {industry}

        Producto:
        {product}

        Módulo:
        {module}

        Descripción del negocio:
        {business_description}

        Utiliza esta información como contexto funcional del SDD.

        Todas las decisiones deben basarse primero en este contexto.

        # REQUERIMIENTO FUNCIONAL

        {requirement}

        # CRITERIOS DE ACEPTACIÓN

        {acceptance_criteria}

        Analiza el requerimiento utilizando el contexto del SDD.

        Extrae únicamente información respaldada por:

        - el SDD
        - el requerimiento
        - los criterios de aceptación

        Si falta información, registra el supuesto en "assumptions".

        No inventes comportamiento del sistema.

        # FORMATO OBLIGATORIO DE RESPUESTA

        {schema}
        """
                
        response = llm_call(
            system_prompt="Eres un QA experto en Risk Based Testing.",
            user_prompt=prompt,
            expect_json=True
        )

        print("\n===== BUSINESS ANALYST OUTPUT =====")
        print(response)
        print("===================================\n")

        return response