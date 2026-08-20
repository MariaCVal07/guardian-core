import pytest

from backend.engines.test_design_engine import RiskMapper


pytestmark = pytest.mark.unit


@pytest.fixture
def mapper():
    return RiskMapper()


class TestMapRisksToTest:

    def test_maps_security_risk_by_keyword(self, mapper):
        risks = ["Riesgo de seguridad en credenciales"]

        covered = mapper.map_risks_to_test(
            "Validar acceso no autorizado",
            "El sistema debe rechazar credenciales inválidas",
            risks
        )

        assert covered == risks

    def test_maps_duplicate_risk_by_keyword(self, mapper):
        risks = ["Riesgo de registros duplicados"]

        covered = mapper.map_risks_to_test(
            "Evitar usuario duplicado",
            "Debe existir un único registro por usuario",
            risks
        )

        assert covered == risks

    def test_does_not_map_unrelated_risk(self, mapper):
        risks = ["Riesgo de saldo negativo"]

        covered = mapper.map_risks_to_test(
            "Login exitoso",
            "Usuario ingresa credenciales válidas",
            risks
        )

        assert covered == []

    def test_empty_risks_returns_empty(self, mapper):
        covered = mapper.map_risks_to_test("cualquier título", "cualquier descripción", [])
        assert covered == []


class TestHasTestForRisk:

    def test_true_when_test_covers_risk(self, mapper):
        tests = [{"covers_risks": ["Riesgo de seguridad"]}]
        assert mapper.has_test_for_risk("riesgo de seguridad", tests) is True

    def test_false_when_no_test_covers_risk(self, mapper):
        tests = [{"covers_risks": ["Riesgo de saldo"]}]
        assert mapper.has_test_for_risk("riesgo de seguridad", tests) is False

    def test_false_when_tests_have_no_covers_risks_key(self, mapper):
        tests = [{"title": "Algún test"}]
        assert mapper.has_test_for_risk("riesgo de seguridad", tests) is False
