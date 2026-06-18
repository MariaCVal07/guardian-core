class RiskAnalystAgent:

    def analyze_risks(
        self,
        analysis
    ):

        risks = analysis.get(
            "potential_risks",
            []
        )

        mitigations = []

        for risk in risks:

            mitigations.append({

                "risk": risk,

                "recommended_mitigation":
                self.generate_mitigation(
                    risk
                )
            })

        return mitigations

    def generate_mitigation(
        self,
        risk
    ):

        risk_lower = risk.lower()

        if "duplicad" in risk_lower:

            return {
                "title":
                "Validar restricción de unicidad",
                "test_type":
                "functional"
            }

        if "saldo" in risk_lower:

            return {
                "title":
                "Validar consistencia de saldo",
                "test_type":
                "functional"
            }

        if "transacción" in risk_lower:

            return {
                "title":
                "Validar integridad de transferencia",
                "test_type":
                "integration"
            }

        if "financiero" in risk_lower:

            return {
                "title":
                "Validar consistencia financiera",
                "test_type":
                "integration"
            }

        if "datos" in risk_lower:

            return {
                "title":
                "Validar persistencia de datos",
                "test_type":
                "integration"
            }

        return {
            "title":
            f"Mitigar {risk}",
            "test_type":
            "functional"
        }