from fastapi import FastAPI
from fastapi import Request
from fastapi import Form

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.automation_engine import AutomationEngine

from backend.agents.business_analyst.agent import (
    BusinessAnalystAgent
)

from backend.risk_engine import RiskEngine
from backend.strategy_engine import StrategyEngine
from backend.test_design_engine import TestDesignEngine

from backend.pipeline import GuardianPipeline


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

    pipeline = GuardianPipeline(

        business_agent=BusinessAnalystAgent(),

        risk_engine=RiskEngine(),

        strategy_engine=StrategyEngine(),

        test_design_engine=TestDesignEngine(),

        automation_engine=AutomationEngine()
    )

    result = pipeline.analyze(

        industry=industry,

        product=product,

        module=module,

        business_description=business_description,

        requirement=requirement,

        acceptance_criteria=acceptance_criteria
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

            "analysis": result["analysis"],

            "risk_score": result["risk_score"],

            "strategy": result["strategy"],

            "test_design": result["test_design"],

            "automation_decisions": result["automation_decisions"],

            "risk_coverage": result["risk_coverage"]
        }
    )