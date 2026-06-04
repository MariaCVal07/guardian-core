class RiskEngine:

    def calculate_risk(

        self,

        industry,

        module,

        requirement
    ):

        score = 0

        industry = industry.lower()
        module = module.lower()
        requirement = requirement.lower()

        # Industria

        if industry in [

            "banca",
            "banking",
            "finanzas",
            "fintech"

        ]:

            score += 40

        elif industry in [

            "salud",
            "healthcare"

        ]:

            score += 35

        elif industry in [

            "ecommerce",
            "retail"

        ]:

            score += 20

        # Módulo

        if module in [

            "wallet",
            "payments",
            "payment",
            "transferencias",
            "transfers"

        ]:

            score += 30

        elif module in [

            "login",
            "autenticacion",
            "authentication"

        ]:

            score += 20

        # Palabras críticas

        critical_words = [

            "dinero",
            "saldo",
            "wallet",
            "credito",
            "payment",
            "transferencia",
            "transfer"
        ]

        for word in critical_words:

            if word in requirement:

                score += 5

        return min(score, 100)