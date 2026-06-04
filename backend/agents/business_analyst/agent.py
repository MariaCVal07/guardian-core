import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)


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

        prompt = f"""
        Eres un QA Senior especializado en:

        - Testing basado en riesgo
        - Risk Based Testing
        - QA Strategy
        - Business Analysis
        - Software Quality Engineering
        - Sistemas financieros
        - Ecommerce
        - Plataformas empresariales

        CONTEXTO DEL NEGOCIO

        Industria:
        {industry}

        Producto:
        {product}

        Módulo:
        {module}

        Descripción:
        {business_description}

        REQUERIMIENTO FUNCIONAL

        {requirement}

        CRITERIOS DE ACEPTACIÓN

        {acceptance_criteria}

        Analiza el requerimiento considerando:

        - Contexto del negocio
        - Riesgo operativo
        - Riesgo financiero
        - Riesgo reputacional
        - Seguridad
        - Integraciones
        - Experiencia de usuario
        - Impacto en producción

        Debes identificar:

        1. Nivel de criticidad
        2. Impacto de negocio
        3. Flujos afectados
        4. Riesgos potenciales
        5. Casos de prueba prioritarios

        RESPONDE EXCLUSIVAMENTE JSON.

        FORMATO OBLIGATORIO:

        {{
            "criticality": "",
            "business_impact": "",
            "affected_flows": [],
            "potential_risks": [],
            "recommended_tests": []
        }}

        El campo criticality solo puede ser:

        - low
        - medium
        - high
        - critical

        El campo recommended_tests debe tener:

        [
            {{
                "test_id": "",
                "title": "",
                "description": "",
                "test_type": "",
                "priority": ""
            }}
        ]

        test_type:

        - functional
        - integration
        - security
        - regression
        - ui
        - api
        - smoke

        priority:

        - low
        - medium
        - high
        - critical

        No agregues markdown.
        No agregues comentarios.
        No agregues texto fuera del JSON.
        """

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": "Eres un QA experto en Risk Based Testing."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        content = response.choices[0].message.content

        return json.loads(content)