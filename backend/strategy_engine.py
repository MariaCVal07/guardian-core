class StrategyEngine:

    def determine_strategy(

        self,

        analysis,

        risk_score
    ):

        strategy = []

        criticality = analysis.get(
            "criticality",
            ""
        ).lower()

        risks = analysis.get(
            "potential_risks",
            []
        )

        recommended_tests = analysis.get(
            "recommended_tests",
            []
        )

        # =====================================
        # Siempre funcional
        # =====================================

        strategy.append(
            "functional"
        )

        # =====================================
        # Estrategia basada en riesgos
        # =====================================

        for risk in risks:

            risk_lower = risk.lower()

            if (
                "seguridad" in risk_lower
                or "autorizado" in risk_lower
                or "credencial" in risk_lower
            ):

                if "security" not in strategy:

                    strategy.append(
                        "security"
                    )

            if (
                "integración" in risk_lower
                or "externo" in risk_lower
                or "pago" in risk_lower
            ):

                if "integration" not in strategy:

                    strategy.append(
                        "integration"
                    )

        # =====================================
        # Estrategia basada en tests sugeridos
        # =====================================

        for test in recommended_tests:

            test_type = test.get(
                "test_type",
                ""
            )

            if (
                test_type == "integration"
                and "integration" not in strategy
            ):

                strategy.append(
                    "integration"
                )

            if (
                test_type == "security"
                and "security" not in strategy
            ):

                strategy.append(
                    "security"
                )

        # =====================================
        # Criticidad alta
        # =====================================

        if criticality in [

            "high",

            "critical"
        ]:

            if "regression" not in strategy:

                strategy.append(
                    "regression"
                )

        # =====================================
        # Criticidad extrema
        # =====================================

        if criticality == "critical":

            if "e2e" not in strategy:

                strategy.append(
                    "e2e"
                )

        return strategy