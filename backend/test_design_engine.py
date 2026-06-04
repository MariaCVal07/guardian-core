class TestDesignEngine:

    def generate_test_design(

        self,

        analysis,

        strategy
    ):

        test_cases = []

        for test in analysis.get(
            "recommended_tests",
            []
        ):

            title = test.get(
                "title",
                ""
            ).lower()

            description = test.get(
                "description",
                ""
            ).lower()

            test_type = test.get(
                "test_type",
                ""
            )

            technique = self.detect_technique(

                title,

                description,

                test_type
            )

            automatable = self.is_automatable(

                test_type,

                technique
            )

            test_cases.append({

                "id": test.get("test_id"),

                "title": test.get("title"),

                "description": test.get("description"),

                "priority": test.get("priority"),

                "test_type": test_type,

                "technique": technique,

                "automatable": automatable
            })

        return test_cases

    def detect_technique(

        self,

        title,

        description,

        test_type
    ):

        text = f"{title} {description}"

        # NEGATIVE TESTING

        if any(word in text for word in [

            "duplicado",
            "duplicada",
            "duplicados",
            "duplicadas",
            "univocidad",
            "única",
            "unica",
            "solo exista",
            "únicamente",
            "unicamente",
            "no permitir",
            "rechazar"

        ]):
            return "Negative Testing"

        # BOUNDARY VALUE

        if any(word in text for word in [

            "saldo",
            "monto",
            "limite",
            "límite",
            "balance"

        ]):

            return "Boundary Value Analysis"

        # SECURITY

        if test_type == "security":

            return "Security Testing"

        # INTEGRATION

        if test_type == "integration":

            return "Integration Testing"

        # REGRESSION

        if test_type == "regression":

            return "Regression Testing"

        # UI

        if test_type == "ui":

            return "UI Validation"

        return "Happy Path"

    def is_automatable(

        self,

        test_type,

        technique
    ):

        if technique in [

            "Happy Path",
            "Negative Testing",
            "Boundary Value Analysis",
            "Integration Testing"

        ]:

            return "Sí"

        if test_type == "security":

            return "Parcial"

        return "No"