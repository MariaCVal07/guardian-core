class StrategyEngine:

    def determine_strategy(self, analysis):

        criticality = analysis.get(
            "criticality",
            ""
        ).lower()

        if criticality == "high":

            return [
                "functional",
                "integration",
                "security"
            ]

        if criticality == "medium":

            return [
                "functional",
                "integration"
            ]

        return [
            "functional"
        ]
        