class RiskEngine:

    def calculate_risk(

        self,

        industry,

        module,

        requirement
    ):

        score = 0

        detected_risks = []

        industry = industry.lower()

        module = module.lower()

        requirement = requirement.lower()

        # ==========================
        # INDUSTRIA
        # ==========================

        if industry in [

            "banca",
            "banking",
            "finanzas",
            "fintech"

        ]:

            score += 40

            detected_risks.append(
                "riesgo financiero"
            )

        elif industry in [

            "salud",
            "healthcare"

        ]:

            score += 35

            detected_risks.append(
                "riesgo regulatorio"
            )

        elif industry in [

            "ecommerce",
            "retail"

        ]:

            score += 20

        # ==========================
        # MODULO
        # ==========================

        if module in [

            "wallet",
            "payments",
            "payment",
            "transferencias",
            "transfers"

        ]:

            score += 30

            detected_risks.append(
                "riesgo de transacción incorrecta"
            )

        elif module in [

            "login",
            "autenticacion",
            "authentication"

        ]:

            score += 20

            detected_risks.append(
                "riesgo de acceso no autorizado"
            )

        # ==========================
        # PALABRAS CLAVE
        # ==========================

        keywords = {

            "saldo":
            "riesgo de saldo incorrecto",

            "wallet":
            "riesgo de wallet duplicada",

            "transfer":
            "riesgo de transferencia errónea",

            "transferencia":
            "riesgo de transferencia errónea",

            "credito":
            "riesgo financiero",

            "payment":
            "riesgo de pago incorrecto",

            "dinero":
            "riesgo financiero"
        }

        for keyword, risk in keywords.items():

            if keyword in requirement:

                score += 5

                if risk not in detected_risks:

                    detected_risks.append(
                        risk
                    )

        return {

            "score": min(score, 100),

            "detected_risks": detected_risks
        }