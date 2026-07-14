class TestClassifier:

    def detect_scenario_type(
        self,
        title,
        description
    ):

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

    def select_design_technique(
        self,
        scenario_type,
        test_type
    ):

        if scenario_type == "Edge Case":
            return "Boundary Value Analysis"

        if scenario_type == "Negative":
            return "Error Guessing"

        if test_type == "integration":
            return "Use Case Testing"

        if test_type == "security":
            return "Threat Based Testing"

        return "Use Case Testing"

    def select_execution_strategy(
        self,
        test_type,
        priority
    ):

        if test_type == "security":
            return "Security"

        if test_type == "integration":
            return "Integration"

        if priority in ["high", "critical"]:
            return "Regression"

        return "Functional"