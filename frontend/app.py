# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi import Request
# pyrefly: ignore [missing-import]
from fastapi import Form

# pyrefly: ignore [missing-import]
from fastapi.responses import HTMLResponse
# pyrefly: ignore [missing-import]
from fastapi.templating import Jinja2Templates
from backend.automation_engine import AutomationEngine

from backend.agents.business_analyst.agent import (
    BusinessAnalystAgent
)

from backend.risk_engine import RiskEngine
from backend.strategy_engine import StrategyEngine
from backend.test_design_engine import TestDesignEngine

app = FastAPI()

templates = Jinja2Templates(
    directory="frontend/templates"
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/analyze", response_class=HTMLResponse)
def analyze(

    request: Request,

    industry: str = Form(...),

    product: str = Form(...),

    module: str = Form(...),

    business_description: str = Form(...),

    requirement: str = Form(...),

    acceptance_criteria: str = Form(...)
):

    # ==================================
    # BUSINESS ANALYSIS
    # ==================================

    agent = BusinessAnalystAgent()

    analysis = agent.analyze_requirement(

        industry,

        product,

        module,

        business_description,

        requirement,

        acceptance_criteria
    )

    # ==================================
    # RISK ENGINE
    # ==================================

    risk_engine = RiskEngine()

    risk_score = risk_engine.calculate_risk(

        industry,

        module,

        requirement
    )

    # ==================================
    # TEST STRATEGY
    # ==================================

    strategy_engine = StrategyEngine()

    strategy = strategy_engine.determine_strategy(

        analysis,

        risk_score
    )

    # ==================================
# TEST DESIGN
# ==================================

    design_engine = TestDesignEngine()

    test_design = design_engine.generate_test_design(
        analysis,
        strategy
    )

    # ==================================
    # AUTOMATION DECISION
    # ==================================

    automation_engine = AutomationEngine()

    automation_decisions = automation_engine.evaluate(
        test_design
    )

    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "industry": industry,
            "product": product,
            "module": module,
            "business_description": business_description,
            "requirement": requirement,
            "acceptance_criteria": acceptance_criteria,
            "analysis": analysis,
            "risk_score": risk_score,
            "strategy": strategy,
            "test_design": test_design,
            "automation_decisions": automation_decisions
        }
    )