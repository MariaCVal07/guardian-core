import pytest

from backend.engines.risk_coverage_engine import RiskCoverageEngine


pytestmark = pytest.mark.unit


@pytest.fixture
def engine():
    return RiskCoverageEngine()


class TestCalculate:

    def test_full_coverage(self, engine):
        risks = [{"title": "Riesgo A"}, {"title": "Riesgo B"}]
        test_design = [
            {"covers_risks": ["Riesgo A"]},
            {"covers_risks": ["Riesgo B"]},
        ]

        result = engine.calculate(risks, test_design)

        assert result["coverage_percent"] == 100
        assert sorted(result["covered_risks"]) == ["Riesgo A", "Riesgo B"]
        assert result["uncovered_risks"] == []
        assert result["total_risks"] == 2

    def test_partial_coverage(self, engine):
        risks = [{"title": "Riesgo A"}, {"title": "Riesgo B"}]
        test_design = [{"covers_risks": ["Riesgo A"]}]

        result = engine.calculate(risks, test_design)

        assert result["coverage_percent"] == 50
        assert result["covered_risks"] == ["Riesgo A"]
        assert result["uncovered_risks"] == ["Riesgo B"]

    def test_no_risks_identified_means_full_coverage_by_convention(self, engine):
        result = engine.calculate([], [])

        assert result["coverage_percent"] == 100
        assert result["total_risks"] == 0

    def test_risk_not_in_original_list_is_ignored(self, engine):
        """
        Un risk_title alucinado por el LLM (que no corresponde a ningún
        riesgo real de identified_risks) no debe inflar la cobertura.
        """
        risks = [{"title": "Riesgo A"}]
        test_design = [{"covers_risks": ["Riesgo Inventado"]}]

        result = engine.calculate(risks, test_design)

        assert result["coverage_percent"] == 0
        assert result["covered_risks"] == []
        assert result["uncovered_risks"] == ["Riesgo A"]

    def test_test_case_without_covers_risks_key_is_handled(self, engine):
        risks = [{"title": "Riesgo A"}]
        test_design = [{"title": "Test sin riesgos mapeados"}]

        result = engine.calculate(risks, test_design)

        assert result["coverage_percent"] == 0
