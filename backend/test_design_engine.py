from backend.risk_mapper import RiskMapper
from backend.test_classifier import TestClassifier

class TestDesignEngine:
    """
    Test Design Agent.

    Responsabilidad:
    Transformar la estrategia de pruebas y los riesgos
    identificados en casos de prueba de alta calidad.

    Especificación funcional:

        backend/agents/test_design/test_design.md

    Contrato de salida:

        backend/agents/test_design/test_design.json

    Actualmente este componente es determinístico
    (Rule Engine), por lo que no utiliza LLM.
    """

    def __init__(self):

        self.risk_mapper = RiskMapper()
        self.classifier = TestClassifier()

    def generate_test_design(
        self,
        analysis
    ):

        tests = []

        counter = 1

        risks = analysis.get(
            "potential_risks",
            []
        )

        for recommendation in analysis["recommended_tests"]:

            title = recommendation.get("title")

            objective = recommendation.get("objective")

            description = recommendation.get("description")

            business_rule = recommendation.get("business_rule")

            risk_covered = recommendation.get("risk_covered")

            scenario = recommendation.get("scenario")

            test_type = recommendation.get("test_type")

            priority = recommendation.get("priority")

            scenario_type = scenario

            design_technique = self.classifier.select_design_technique(
                scenario_type,
                test_type
            )

            execution_strategy = self.classifier.select_execution_strategy(
                test_type,
                priority
            )

            covered_risks = [risk_covered] if risk_covered else []

            if not risk_covered:

                covered_risks = self.risk_mapper.map_risks_to_test(
                    title,
                    description,
                    risks
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

                "automatable": self.is_automatable(
                    test_type
                ),

                "objective": objective,

                "business_rule": business_rule,

                "risk_covered": risk_covered,

                "covers_risks": covered_risks
            })

            counter += 1

        return tests

    def is_automatable(
        self,
        test_type
    ):

        if test_type == "security":

            return "Parcial"

        return "Sí"