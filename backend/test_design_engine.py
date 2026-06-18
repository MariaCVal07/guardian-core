class TestDesignEngine:

    def generate_test_design(
        self,
        analysis,
        strategy
    ):

        tests = []

        counter = 1

        risks = analysis.get(
            "potential_risks",
            []
        )

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

            covered_risks = self.map_risks_to_test(
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

                "covers_risks": covered_risks
            })

            counter += 1

        for risk in risks:

            if not self.has_test_for_risk(
                risk,
                tests
            ):

                tests.append(
                    self.create_risk_based_test(
                        risk,
                        counter
                    )
                )

                counter += 1

        return tests

    def has_test_for_risk(
        self,
        risk,
        tests
    ):

        risk = risk.lower()

        for test in tests:

            for covered in test.get(
                "covers_risks",
                []
            ):

                if risk == covered.lower():

                    return True

        return False

    def map_risks_to_test(
    self,
    title,
    description,
    risks
    ):

        text = f"{title} {description}".lower()

        covered = []

        for risk in risks:

            risk_lower = risk.lower()

            if "seguridad" in risk_lower:

                if (
                    "seguridad" in text
                    or "segura" in text
                    or "autorizado" in text
                    or "inyección" in text
                ):
                    covered.append(risk)

            elif "datos" in risk_lower:

                if (
                    "datos" in text
                    or "persistencia" in text
                    or "almacenamiento" in text
                    or "backup" in text
                    or "recuperación" in text
                ):
                    covered.append(risk)

            elif "duplicad" in risk_lower:

                if (
                    "duplicad" in text
                    or "unicidad" in text
                    or "único" in text
                ):
                    covered.append(risk)

            elif "saldo" in risk_lower:

                if "saldo" in text:
                    covered.append(risk)

            elif "transacción" in risk_lower:

                if (
                    "transferencia" in text
                    or "transacción" in text
                    or "operación financiera" in text
                ):
                    covered.append(risk)

            elif "financiero" in risk_lower:

                if (
                    "financiera" in text
                    or "movimientos" in text
                    or "transferencia" in text
                ):
                    covered.append(risk)

            elif "integración" in risk_lower:

                if (
                    "integración" in text
                    or "integración con otros módulos" in text
                    or "otros módulos" in text
                ):
                    covered.append(risk)

        return covered

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

    def create_risk_based_test(
        self,
        risk,
        counter
    ):

        risk_lower = risk.lower()
        print("RISK DETECTADO:", risk_lower)

        if "duplicad" in risk_lower:

            return {

                "id": f"T{counter:03}",

                "title":
                "Validar restricción de unicidad",

                "description":
                "Verificar que no sea posible crear registros duplicados",

                "scenario_type":
                "Negative",

                "design_technique":
                "Risk Based Testing",

                "execution_strategy":
                "Regression",

                "priority":
                "high",

                "test_type":
                "functional",

                "automatable":
                "Sí",

                "covers_risks":
                [risk]
            }

        if "saldo" in risk_lower:

            return {

                "id": f"T{counter:03}",

                "title":
                "Validar consistencia de saldo",

                "description":
                "Verificar cálculos y persistencia correcta del saldo",

                "scenario_type":
                "Edge Case",

                "design_technique":
                "Risk Based Testing",

                "execution_strategy":
                "Regression",

                "priority":
                "high",

                "test_type":
                "functional",

                "automatable":
                "Sí",

                "covers_risks":
                [risk]
            }

        if (
            "pérdida de datos" in risk_lower
            or "datos" in risk_lower
            ):

            return {

                "id": f"T{counter:03}",

                "title":
                "Validar persistencia de datos del cliente",

                "description":
                "Verificar que la información del cliente permanezca íntegra después de operaciones de creación, actualización y consulta",

                "scenario_type":
                "Positive",

                "design_technique":
                "Risk Based Testing",

                "execution_strategy":
                "Regression",

                "priority":
                "high",

                "test_type":
                "integration",

                "automatable":
                "Sí",

                "covers_risks":
                [risk]
            }

        if "transacción" in risk_lower:

            return {

                "id": f"T{counter:03}",

                "title":
                "Validar integridad de transferencia",

                "description":
                "Verificar consistencia de la operación financiera",

                "scenario_type":
                "Positive",

                "design_technique":
                "Risk Based Testing",

                "execution_strategy":
                "Regression",

                "priority":
                "high",

                "test_type":
                "integration",

                "automatable":
                "Sí",

                "covers_risks":
                [risk]
            }

        if "financiero" in risk_lower:

            return {

                "id": f"T{counter:03}",

                "title":
                "Validar consistencia financiera",

                "description":
                "Verificar que los movimientos financieros sean correctos",

                "scenario_type":
                "Positive",

                "design_technique":
                "Risk Based Testing",

                "execution_strategy":
                "Regression",

                "priority":
                "high",

                "test_type":
                "functional",

                "automatable":
                "Sí",

                "covers_risks":
                [risk]
            }

        return {
             "id": f"T{counter:03}",

            "title":
            f"Validar control para {risk}",

            "description":
            f"Verificar controles asociados a {risk}",

            "scenario_type":
            "Risk Based",

            "design_technique":
            "Risk Based Testing",

            "execution_strategy":
            "Regression",

            "priority":
            "high",

            "test_type":
            "functional",

            "automatable":
            "Sí",

            "covers_risks":
            [risk]
        }

    def is_automatable(
        self,
        test_type
    ):

        if test_type == "security":

            return "Parcial"

        return "Sí"