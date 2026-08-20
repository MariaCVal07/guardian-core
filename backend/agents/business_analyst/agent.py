from backend.core.llm_client import llm_call
from backend.core.loaders import load_prompt, load_schema
from backend.validators.business_model_normalizer import normalize_business_model


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

        # Enumerar criterios de aceptación
        criteria_lines = [
            line.strip()
            for line in acceptance_criteria.split("\n")
            if line.strip()
        ]

        criteria_text = "\n".join(
            [
                f"AC-{i+1:02d}: {line}"
                for i, line in enumerate(criteria_lines)
            ]
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

        # REQUERIMIENTO FUNCIONAL

        {requirement}

        # CRITERIOS DE ACEPTACIÓN

        {criteria_text}

        # INSTRUCCIONES

        Utiliza únicamente la información del SDD, el requerimiento y los criterios de aceptación.

        {schema}
        """

        response = llm_call(
            system_prompt="""
            Eres un Senior Business Analyst especializado en Domain Modeling.

            Construye únicamente un modelo funcional del dominio.

            No inventes información.
            No inventes actores.
            No inventes entidades.
            No inventes reglas.
            No inventes estados.
            No completes procesos.

            Si una información no puede justificarse mediante evidencia explícita,
            simplemente omítela.

            Responde siempre en el mismo idioma del contexto recibido (Business Model, Risk Model, Test Strategy o SDD original). Si el contexto está en español, responde en español. Si está en otro idioma, responde en ese idioma. Nunca traduzcas el contenido recibido. Los nombres de los campos JSON (keys) deben mantenerse siempre en inglés, tal como los define el schema.

            Responde únicamente utilizando el JSON solicitado.
            """,
            user_prompt=prompt,
            expect_json=True
        )

        response = normalize_business_model(response)

        print("\n===== BUSINESS ANALYST OUTPUT =====")
        print(response)
        print("===================================\n")

        return response