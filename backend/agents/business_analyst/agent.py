import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",

    api_key=os.getenv("GROQ_API_KEY")
)


class BusinessAnalystAgent:

    def analyze_requirement(self, requirement: str):

        prompt = f"""
            Eres un QA Senior especializado en:

            - análisis estratégico de negocio
            - testing basado en riesgo
            - prevención de regresiones críticas
            - protección de flujos core del negocio
            - estabilidad de releases
            - impacto operacional
            - validación de integraciones críticas
            - análisis de riesgo funcional y financiero

            Tu objetivo NO es únicamente validar funcionalidades.

            Tu responsabilidad es proteger el negocio identificando:
            - riesgos críticos
            - impactos operacionales
            - posibles regresiones
            - fallas en flujos sensibles
            - afectaciones financieras
            - problemas de seguridad
            - impactos en experiencia de usuario

            Analiza el siguiente requerimiento:

            {requirement}

            Debes identificar:

            1. Nivel de criticidad
            2. Impacto de negocio
            3. Flujos afectados
            4. Riesgos potenciales
            5. Casos de prueba prioritarios

            REGLAS IMPORTANTES:

            - Debes responder EXCLUSIVAMENTE JSON válido
            - NO agregues explicaciones
            - NO agregues comentarios
            - NO agregues markdown
            - NO agregues bloque ```json
            - NO agregues texto antes o después del JSON
            - La respuesta debe iniciar con {{
            - La respuesta debe finalizar con }}

            Las keys del JSON deben ser EXACTAMENTE estas:

            {{
                "criticality": "",
                "business_impact": "",
                "affected_flows": [],
                "potential_risks": [],
                "recommended_tests": []
            }}

            NO cambies:
            - nombres de propiedades
            - idioma de propiedades
            - estructura del JSON

            El campo "criticality" solo puede tener:
            - low
            - medium
            - high
            - critical

            El campo "recommended_tests" debe contener una lista de objetos con esta estructura EXACTA:

            [
                {{
                    "test_id": "",
                    "title": "",
                    "description": "",
                    "test_type": "",
                    "priority": ""
                }}
            ]

            El campo "priority" solo puede tener:
            - low
            - medium
            - high
            - critical

            El campo "test_type" solo puede tener:
            - functional
            - integration
            - security
            - regression
            - ui
            - api
            - smoke

            Genera casos de prueba basados en:
            - criticidad del negocio
            - impacto operacional
            - riesgo financiero
            - seguridad
            - integraciones
            - estabilidad del release
            """

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": "Eres un QA experto."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        import json

        content = response.choices[0].message.content

        return json.loads(content)