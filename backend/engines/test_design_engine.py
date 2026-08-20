class TestClassifier:
    """
    Test Classification Rules.
    
    Responsabilidad:
    Clasificar escenarios de prueba y seleccionar técnicas de diseño.
    """

    def detect_scenario_type(self, title, description):
        """
        Detecta el tipo de escenario: Positive, Negative o Edge Case.
        """
        text = f"{title} {description}".lower()

        if (
            "duplicad" in text
            or "inválido" in text
            or "rechazar" in text
            or "bloquear" in text
        ):
            return "Negative"

        if (
            "límite" in text
            or "máximo" in text
            or "mínimo" in text
            or "saldo" in text
        ):
            return "Edge Case"

        return "Positive"

    def select_design_technique(self, scenario_type, test_type):
        """
        Selecciona la técnica de diseño basada en tipo de escenario y prueba.
        """
        if scenario_type in ("edge_case", "boundary"):
            return "Boundary Value Analysis"

        if scenario_type == "negative":
            return "Error Guessing"

        if test_type == "integration":
            return "Use Case Testing"

        if test_type == "security":
            return "Threat Based Testing"

        return "Use Case Testing"

    def select_execution_strategy(self, test_type, priority):
        """
        Selecciona la estrategia de ejecución basada en tipo y prioridad.
        """
        if test_type == "security":
            return "Security"

        if test_type == "integration":
            return "Integration"

        if priority in ["high", "critical"]:
            return "Regression"

        return "Functional"


class RiskMapper:
    """
    Risk Mapping Rules.
    
    Responsabilidad:
    Mapear riesgos identificados a casos de prueba.
    """

    def map_risks_to_test(self, title, description, risks):
        """
        Mapea riesgos a pruebas basado en coincidencia de palabras clave.
        """
        text = f"{title} {description}".lower()
        covered = []

        for risk in risks:
            risk_lower = risk.lower()

            if "seguridad" in risk_lower:
                if (
                    "seguridad" in text
                    or "credencial" in text
                    or "autorizado" in text
                    or "dato" in text
                ):
                    covered.append(risk)

            elif "duplicad" in risk_lower:
                if (
                    "duplicad" in text
                    or "único" in text
                    or "un solo" in text
                ):
                    covered.append(risk)

            elif "saldo" in risk_lower:
                if "saldo" in text:
                    covered.append(risk)

            elif (
                "transacción" in risk_lower
                or "transferencia" in risk_lower
            ):
                if (
                    "transferencia" in text
                    or "transacción" in text
                ):
                    covered.append(risk)

            elif "financiero" in risk_lower:
                if (
                    "financiero" in text
                    or "saldo" in text
                ):
                    covered.append(risk)

            elif (
                "datos" in risk_lower
                or "usuario" in risk_lower
                or "cliente" in risk_lower
            ):
                if (
                    "usuario" in text
                    or "cliente" in text
                    or "dato" in text
                ):
                    covered.append(risk)

        return covered

    def has_test_for_risk(self, risk, tests):
        """
        Verifica si existe un caso de prueba que cubre un riesgo específico.
        """
        risk = risk.lower()

        for test in tests:
            for covered in test.get("covers_risks", []):
                if risk == covered.lower():
                    return True

        return False


class TestDesignEngine:
    """
    Test Design Engine.

    Responsabilidad:
    Transformar la estrategia de pruebas y los riesgos
    identificados en casos de prueba de alta calidad.

    Especificación funcional:
        backend/agents/test_design/test_design.md

    Contrato de salida:
        backend/agents/test_design/test_design.json

    Este componente es determinístico (Rule Engine),
    no utiliza LLM.
    """

    def __init__(self):
        """Inicializa los sub-engines (clasificador y mapeador de riesgos)."""
        self.risk_mapper = RiskMapper()
        self.classifier = TestClassifier()

    def generate_test_design(self, analysis, risk_analysis):
        """
        Genera diseño de pruebas a partir del análisis funcional.

        Args:
            analysis: Dict con análisis funcional y recomendaciones de pruebas
            risk_analysis: Dict con los riesgos identificados (risk_analyst.json),
                usado como respaldo para mapear riesgos por palabras clave
                cuando una recomendación no trae su propio risk_title.

        Returns:
            List de casos de prueba diseñados
        """
        tests = []
        counter = 1

        identified_risks = risk_analysis.get("identified_risks", [])
        risk_titles = [
            risk.get("title")
            for risk in identified_risks
            if risk.get("title")
        ]

        for recommendation in analysis["recommended_tests"]:
            title = recommendation.get("title")
            objective = recommendation.get("objective")
            description = recommendation.get("description")
            business_rule = recommendation.get("business_rule")
            risk_covered = recommendation.get("risk_title")
            scenario = recommendation.get("scenario")
            test_type = recommendation.get("test_type")
            priority = recommendation.get("priority")

            scenario_type = scenario

            # Selecciona técnica de diseño basada en escenario y tipo
            design_technique = self.classifier.select_design_technique(
                scenario_type,
                test_type
            )

            # Selecciona estrategia de ejecución basada en tipo y prioridad
            execution_strategy = self.classifier.select_execution_strategy(
                test_type,
                priority
            )

            # Mapea riesgos cubiertos por esta prueba
            covered_risks = [risk_covered] if risk_covered else []

            if not risk_covered:
                covered_risks = self.risk_mapper.map_risks_to_test(
                    title,
                    description,
                    risk_titles
                )

            tests.append({
                "id": f"T{counter:03}",
                "title": title,
                "description": description,
                "scenario_type": scenario_type,
                "design_technique": design_technique,
                "execution_strategy": execution_strategy,
                "priority": priority,
                "test_type": test_type,
                "automatable": self.is_automatable(test_type),
                "objective": objective,
                "business_rule": business_rule,
                "risk_covered": risk_covered,
                "covers_risks": covered_risks
            })

            counter += 1

        return tests

    def is_automatable(self, test_type):
        """
        Determina si un tipo de prueba es automatizable.
        
        Args:
            test_type: Tipo de prueba (security, functional, etc.)
            
        Returns:
            "Sí" o "Parcial" según el tipo
        """
        if test_type == "security":
            return "Parcial"

        return "Sí"