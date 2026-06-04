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

        # Riesgo muy alto

        if risk_score >= 80:

            strategy.extend([

                "functional",

                "integration",

                "security",

                "regression",

                "e2e"
            ])

        # Riesgo medio

        elif risk_score >= 50:

            strategy.extend([

                "functional",

                "integration",

                "regression"
            ])

        # Riesgo bajo

        else:

            strategy.extend([

                "functional"
            ])

        # Refuerzo por criticidad detectada por IA

        if criticality == "critical":

            if "security" not in strategy:
                strategy.append("security")

            if "e2e" not in strategy:
                strategy.append("e2e")

        return strategy