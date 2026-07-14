class RiskMapper:

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