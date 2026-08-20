import pytest

from backend.validators.business_model_normalizer import normalize_business_model


pytestmark = pytest.mark.unit


class TestNormalizeBusinessModel:

    def test_none_input_does_not_crash_and_guarantees_list_fields(self):
        """
        Regresión: si el LLM del Business Analyst falla (llm_call
        devuelve None), normalize_business_model recibía None y hacía
        'return {}' inmediatamente, sin garantizar 'actors', 'entities',
        etc. como listas. Eso rompía el template (itera esas claves).
        """
        result = normalize_business_model(None)

        for field in ["actors", "entities", "business_rules", "relationships"]:
            assert result[field] == []

    def test_empty_dict_input_gets_list_fields_filled(self):
        result = normalize_business_model({})

        assert result["actors"] == []
        assert result["invariants"] == []

    def test_deduplicates_simple_lists(self):
        model = {"actors": ["Cliente", "Cliente", " Cliente "]}

        result = normalize_business_model(model)

        assert result["actors"] == ["Cliente"]

    def test_normalizes_relationships_and_drops_incomplete_ones(self):
        model = {
            "relationships": [
                {"source": " Cliente ", "relationship": " tiene ", "target": " Cuenta "},
                {"source": "Cliente"},
            ]
        }

        result = normalize_business_model(model)

        assert result["relationships"] == [
            {"source": "Cliente", "relationship": "tiene", "target": "Cuenta"}
        ]

    def test_normalizes_business_rules_dict_and_string_forms(self):
        model = {
            "business_rules": [
                {"rule": " El saldo no puede ser negativo ", "evidence": " AC-01 "},
                "El usuario debe estar autenticado",
                {"rule": "", "evidence": "AC-02"},
            ]
        }

        result = normalize_business_model(model)

        assert result["business_rules"] == [
            {"rule": "El saldo no puede ser negativo", "evidence": "AC-01"},
            {"rule": "El usuario debe estar autenticado", "evidence": ""},
        ]

    def test_removes_constraints_and_invariants_duplicated_as_rules(self):
        model = {
            "business_rules": [{"rule": "El saldo no puede ser negativo", "evidence": ""}],
            "constraints": ["El saldo no puede ser negativo", "Máximo 3 intentos"],
            "invariants": ["El saldo no puede ser negativo"],
        }

        result = normalize_business_model(model)

        assert result["constraints"] == ["Máximo 3 intentos"]
        assert result["invariants"] == []
