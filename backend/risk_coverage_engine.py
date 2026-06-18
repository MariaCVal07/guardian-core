class RiskCoverageEngine:

    def calculate(

        self,

        risks,

        test_design
    ):

        covered_risks = set()

        for test_case in test_design:

            for risk in test_case.get(

                "covers_risks",

                []
            ):

                covered_risks.add(risk)

        all_risks = set(risks)

        uncovered_risks = all_risks - covered_risks

        if len(all_risks) == 0:

            coverage_percent = 100

        else:

            coverage_percent = int(

                (len(covered_risks) / len(all_risks))

                * 100
            )

        return {

            "total_risks": len(all_risks),

            "covered_risks": list(covered_risks),

            "uncovered_risks": list(uncovered_risks),

            "coverage_percent": coverage_percent
        }
        