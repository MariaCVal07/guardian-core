from fastapi import FastAPI
from fastapi import Request
from fastapi import Form

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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

            "test_design": test_design
        }
    )