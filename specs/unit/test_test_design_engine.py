import pytest

from backend.engines.test_design_engine import TestDesignEngine as GuardianTestDesignEngine


pytestmark = pytest.mark.unit


@pytest.fixture
def engine():
    return GuardianTestDesignEngine()


def make_recommendation(**overrides):
    base = {
        "title": "Verificar login exitoso",
        "objective": "Confirmar acceso con credenciales válidas",
        "description": "Usuario ingresa credenciales correctas",
        "business_rule": "El usuario debe autenticarse antes de acceder",
        "risk_title": "Riesgo de acceso no autorizado",
        "scenario": "happy_path",
        "test_type": "functional",
        "priority": "high",
    }
    base.update(overrides)
    return base


class TestGenerateTestDesign:

    def test_uses_risk_title_from_recommendation_as_covers_risks(self, engine):
        """
        Regresión del bug crítico del audit: TestDesignEngine leía
        'risk_covered', pero el contrato real de test_design.json
        (producido por TestDesignerAgent) usa 'risk_title'.
        """
        analysis = {"recommended_tests": [make_recommendation()]}
        risk_analysis = {"identified_risks": [
            {"title": "Riesgo de acceso no autorizado"}
        ]}

        tests = engine.generate_test_design(analysis, risk_analysis)

        assert len(tests) == 1
        assert tests[0]["covers_risks"] == ["Riesgo de acceso no autorizado"]

    def test_falls_back_to_keyword_mapping_when_risk_title_missing(self, engine):
        recommendation = make_recommendation(
            risk_title=None,
            title="Rechazar usuario duplicado",
            description="El sistema no debe permitir credenciales duplicadas",
        )
        analysis = {"recommended_tests": [recommendation]}
        risk_analysis = {"identified_risks": [
            {"title": "Riesgo de registros duplicados"}
        ]}

        tests = engine.generate_test_design(analysis, risk_analysis)

        assert tests[0]["covers_risks"] == ["Riesgo de registros duplicados"]

    def test_no_identified_risks_yields_no_covered_risks(self, engine):
        analysis = {"recommended_tests": [make_recommendation(risk_title=None)]}
        risk_analysis = {"identified_risks": []}

        tests = engine.generate_test_design(analysis, risk_analysis)

        assert tests[0]["covers_risks"] == []

    def test_scenario_vocabulary_drives_design_technique(self, engine):
        """
        Regresión del bug de vocabulario: antes de la corrección,
        design_technique siempre caía al valor por defecto porque
        comparaba contra 'Edge Case'/'Negative' en vez de los valores
        reales del schema ('edge_case'/'negative').
        """
        analysis = {"recommended_tests": [
            make_recommendation(scenario="edge_case", test_type="functional"),
        ]}
        risk_analysis = {"identified_risks": []}

        tests = engine.generate_test_design(analysis, risk_analysis)

        assert tests[0]["design_technique"] == "Boundary Value Analysis"

    def test_ids_are_generated_sequentially(self, engine):
        analysis = {"recommended_tests": [
            make_recommendation(), make_recommendation()
        ]}
        risk_analysis = {"identified_risks": []}

        tests = engine.generate_test_design(analysis, risk_analysis)

        assert [t["id"] for t in tests] == ["T001", "T002"]

    def test_security_test_type_is_only_partially_automatable(self, engine):
        analysis = {"recommended_tests": [
            make_recommendation(test_type="security")
        ]}
        risk_analysis = {"identified_risks": []}

        tests = engine.generate_test_design(analysis, risk_analysis)

        assert tests[0]["automatable"] == "Parcial"
