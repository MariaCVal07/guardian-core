class AutomationEngine:

    def evaluate(self, test_design):

        decisions = []

        for test_case in test_design:

            technique = test_case.get(
                "design_technique",
                ""
            )

            test_type = test_case.get(
                "test_type",
                ""
            )

            decision = self.decide(
                technique,
                test_type
            )

            decisions.append({

                "id": test_case["id"],

                "title": test_case["title"],

                "decision": decision["decision"],

                "reason": decision["reason"]
            })

        return decisions

    def decide(
        self,
        technique,
        test_type
    ):

        if technique in [

            "Boundary Value Analysis",
            "Use Case Testing"

        ]:

            return {

                "decision": "Automatizar",

                "reason":
                "Escenario estable y repetible."
            }

        if test_type == "integration":

            return {

                "decision": "Automatizar",

                "reason":
                "Validación frecuente entre sistemas."
            }

        if test_type == "security":

            return {

                "decision": "Parcial",

                "reason":
                "Requiere herramientas especializadas."
            }

        if test_type == "ui":

            return {

                "decision": "Manual",

                "reason":
                "Alta variabilidad visual."
            }

        return {

            "decision": "Manual",

            "reason":
            "No genera suficiente retorno automatizar."
        }