import pytest
from unittest.mock import patch

from backend.pipeline import GuardianPipeline
from backend.agents.business_analyst.agent import BusinessAnalystAgent
from backend.agents.risk_analyst.agent import RiskAnalystAgent
from backend.agents.strategy.strategy_engine import StrategyEngine
from backend.agents.test_designer.agent import TestDesignerAgent
from backend.agents.automation.automation_engine import AutomationEngine
from backend.engines.test_design_engine import TestDesignEngine as GuardianTestDesignEngine


pytestmark = pytest.mark.integration


BUSINESS_MODEL = {
    "business_goal": "Permitir acceso seguro al inventario",
    "business_impact": "alto",
    "criticality": "high",
    "actors": ["Usuario"],
    "entities": ["Cuenta"],
    "relationships": [],
    "business_rules": [
        {"rule": "El usuario debe autenticarse antes de ver el inventario", "evidence": "AC-01"}
    ],
    "constraints": [],
    "preconditions": [],
    "postconditions": [],
    "valid_states": [],
    "invalid_states": [],
    "functional_flow": [],
    "ambiguities": [],
    "missing_information": [],
    "invariants": [],
    "assumptions": [],
}

RISK_MODEL = {
    "identified_risks": [
        {
            "title": "Riesgo de acceso no autorizado",
            "description": "Un usuario no autenticado accede al inventario",
            "category": "security",
            "related_rule": "El usuario debe autenticarse antes de ver el inventario",
            "risk_source": "business_rule",
            "recommended_mitigation": {
                "description": "Validar sesión antes de mostrar el inventario",
                "test_type": "security",
            },
        }
    ]
}

STRATEGY = {
    "risk_strategies": [
        {
            "risk_title": "Riesgo de acceso no autorizado",
            "priority": "high",
            "recommended_test_type": "security",
            "test_objectives": [
                {
                    "id": "OBJ-001",
                    "scenario": "negative",
                    "objective": "Confirmar que el acceso sin sesión es rechazado",
                    "reason": "Mitiga el riesgo de acceso no autorizado",
                }
            ],
            "justification": "El riesgo es de categoría security y alta prioridad",
        }
    ]
}

TESTS = {
    "tests": [
        {
            "id": "TC-001",
            "title": "Rechazar acceso al inventario sin sesión válida",
            "objective": "Confirmar que el acceso sin sesión es rechazado",
            "description": "Un usuario sin sesión intenta acceder al inventario",
            "business_rule": "El usuario debe autenticarse antes de ver el inventario",
            "risk_title": "Riesgo de acceso no autorizado",
            "scenario": "negative",
            "test_type": "security",
            "priority": "high",
        }
    ]
}

AUTOMATION = {
    "automation_decisions": [
        {
            "id": "TC-001",
            "title": "Rechazar acceso al inventario sin sesión válida",
            "decision": "Automatizar",
            "reason": "Es un flujo crítico de seguridad, apto para automatización",
            "business_rule": "El usuario debe autenticarse antes de ver el inventario",
            "risk_covered": "Riesgo de acceso no autorizado",
        }
    ]
}


def build_pipeline():
    return GuardianPipeline(
        business_agent=BusinessAnalystAgent(),
        risk_analyst=RiskAnalystAgent(),
        strategy_engine=StrategyEngine(),
        test_design_engine=GuardianTestDesignEngine(),
        automation_engine=AutomationEngine(),
        test_designer=TestDesignerAgent(),
    )


@patch("backend.agents.automation.automation_engine.llm_call", return_value=AUTOMATION)
@patch("backend.agents.test_designer.agent.llm_call", return_value=TESTS)
@patch("backend.agents.strategy.strategy_engine.llm_call", return_value=STRATEGY)
@patch("backend.agents.risk_analyst.agent.llm_call", return_value=RISK_MODEL)
@patch("backend.agents.business_analyst.agent.llm_call", return_value=BUSINESS_MODEL)
def test_pipeline_end_to_end_produces_full_risk_coverage(
    mock_business, mock_risk, mock_strategy, mock_tests, mock_automation
):
    """
    Prueba de regresión del bug crítico del audit: con un test que
    declara risk_title='Riesgo de acceso no autorizado' (el mismo
    título emitido por el Risk Analyst), la cobertura de riesgo debe
    llegar a 100%, no a 0% como ocurría antes de la corrección.
    """
    pipeline = build_pipeline()

    result = pipeline.analyze(
        industry="fintech",
        product="Guardian Bank App",
        module="inventario",
        business_description="Aplicación de banca móvil",
        requirement="Cuando un usuario realiza login correcto debe acceder al inventario",
        acceptance_criteria="AC-01: El usuario debe estar autenticado",
    )

    assert result["risk_coverage"]["coverage_percent"] == 100
    assert result["risk_coverage"]["uncovered_risks"] == []
    assert result["test_design"][0]["covers_risks"] == ["Riesgo de acceso no autorizado"]
    assert result["test_design"][0]["design_technique"] == "Error Guessing"
    assert result["automation_decisions"][0]["decision"] == "Automatizar"


@patch("backend.agents.automation.automation_engine.llm_call", return_value=None)
@patch("backend.agents.test_designer.agent.llm_call", return_value=None)
@patch("backend.agents.strategy.strategy_engine.llm_call", return_value=None)
@patch("backend.agents.risk_analyst.agent.llm_call", return_value=None)
@patch("backend.agents.business_analyst.agent.llm_call", return_value=None)
def test_pipeline_survives_total_llm_failure(
    mock_business, mock_risk, mock_strategy, mock_tests, mock_automation
):
    """
    Si el LLM falla en todas las etapas (llm_call devuelve None),
    el pipeline no debe lanzar una excepción; debe degradar a
    resultados vacíos pero con la forma de contrato esperada.
    """
    pipeline = build_pipeline()

    result = pipeline.analyze(
        industry="fintech",
        product="Guardian Bank App",
        module="inventario",
        business_description="Aplicación de banca móvil",
        requirement="Cuando un usuario realiza login correcto debe acceder al inventario",
        acceptance_criteria="AC-01: El usuario debe estar autenticado",
    )

    assert result["risk_analysis"] == {"identified_risks": []}
    assert result["strategy"] == {"risk_strategies": []}
    assert result["test_design"] == []
    assert result["automation_decisions"] == []
    assert result["risk_coverage"]["coverage_percent"] == 100
