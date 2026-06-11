class TestDesignEngine:

    def generate_test_design(
        self,
        analysis,
        strategy
    ):

        tests = []

        counter = 1

        for recommendation in analysis["recommended_tests"]:

            title = recommendation["title"]

            description = recommendation["description"]

            test_type = recommendation["test_type"]

            priority = recommendation["priority"]

            scenario_type = self.detect_scenario_type(
                title,
                description
            )

            design_technique = self.select_design_technique(
                scenario_type,
                test_type
            )

            execution_strategy = self.select_execution_strategy(
                test_type,
                priority
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
                )
            })

            counter += 1

        return tests

    def detect_scenario_type(
        self,
        title,
        description
    ):

        text = f"{title} {description}".lower()

        if (
            "duplicada" in text
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

    def is_automatable(
        self,
        test_type
    ):

        if test_type == "security":

            return "Parcial"

        return "Sí"