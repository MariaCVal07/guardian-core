from backend.core.llm_client import llm_call
from backend.core.loaders import load_prompt, load_schema

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

        base_prompt = load_prompt("business_analyst.md")

        schema = load_schema("business_analyst.json")  

        print(base_prompt[:500])
        print(schema)

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
            system_prompt="""
                Eres un Senior Business Analyst y Domain Modeling Expert.

                Tu única responsabilidad es construir un modelo funcional del dominio.

                Nunca diseñes pruebas.

                Nunca identifiques riesgos.

                Nunca propongas estrategias.

                Nunca inventes comportamiento.

                Extrae únicamente información respaldada por el contexto.
                """,
                
            user_prompt=prompt,
            expect_json=True
        )

        print("\n===== BUSINESS ANALYST OUTPUT =====")
        print(response)
        print("===================================\n")
        
        return response
