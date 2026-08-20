import pytest

from backend.engines.test_design_engine import TestClassifier


pytestmark = pytest.mark.unit


@pytest.fixture
def classifier():
    return TestClassifier()


class TestDetectScenarioType:

    def test_detects_negative_by_keyword(self, classifier):
        assert classifier.detect_scenario_type(
            "Rechazar usuario duplicado", ""
        ) == "Negative"

    def test_detects_edge_case_by_keyword(self, classifier):
        assert classifier.detect_scenario_type(
            "Validar saldo mínimo permitido", ""
        ) == "Edge Case"

    def test_defaults_to_positive(self, classifier):
        assert classifier.detect_scenario_type(
            "Login exitoso", "Usuario ingresa credenciales válidas"
        ) == "Positive"


class TestSelectDesignTechnique:
    """
    El vocabulario real de 'scenario' viene de test_design.json:
    happy_path | negative | edge_case | alternate | boundary.
    Estos tests protegen contra volver a desalinear ese vocabulario
    con el usado internamente por el classifier.
    """

    @pytest.mark.parametrize("scenario_type", ["edge_case", "boundary"])
    def test_boundary_scenarios_use_boundary_value_analysis(
        self, classifier, scenario_type
    ):
        assert classifier.select_design_technique(
            scenario_type, "functional"
        ) == "Boundary Value Analysis"

    def test_negative_scenario_uses_error_guessing(self, classifier):
        assert classifier.select_design_technique(
            "negative", "functional"
        ) == "Error Guessing"

    def test_integration_test_type_uses_use_case_testing(self, classifier):
        assert classifier.select_design_technique(
            "happy_path", "integration"
        ) == "Use Case Testing"

    def test_security_test_type_uses_threat_based_testing(self, classifier):
        assert classifier.select_design_technique(
            "happy_path", "security"
        ) == "Threat Based Testing"

    def test_happy_path_functional_defaults_to_use_case_testing(
        self, classifier
    ):
        assert classifier.select_design_technique(
            "happy_path", "functional"
        ) == "Use Case Testing"


class TestSelectExecutionStrategy:

    def test_security_test_type(self, classifier):
        assert classifier.select_execution_strategy(
            "security", "low"
        ) == "Security"

    def test_integration_test_type(self, classifier):
        assert classifier.select_execution_strategy(
            "integration", "low"
        ) == "Integration"

    @pytest.mark.parametrize("priority", ["high", "critical"])
    def test_high_or_critical_priority_uses_regression(
        self, classifier, priority
    ):
        assert classifier.select_execution_strategy(
            "functional", priority
        ) == "Regression"

    def test_defaults_to_functional(self, classifier):
        assert classifier.select_execution_strategy(
            "functional", "low"
        ) == "Functional"
