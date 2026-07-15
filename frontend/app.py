from fastapi import FastAPI
from fastapi import Request
from fastapi import Form

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.pipeline import GuardianPipeline

from backend.agents.business_analyst.agent import BusinessAnalystAgent
from backend.agents.risk_analyst.agent import RiskAnalystAgent
from backend.agents.test_designer.agent import TestDesignerAgent

from backend.strategy_engine import StrategyEngine
from backend.test_design_engine import TestDesignEngine
from backend.automation_engine import AutomationEngine


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
    print("ENTRÓ AL ENDPOINT /analyze")

    pipeline = GuardianPipeline(

        business_agent=BusinessAnalystAgent(),

        risk_analyst=RiskAnalystAgent(),

        strategy_engine=StrategyEngine(),

        test_design_engine=TestDesignEngine(),

        automation_engine=AutomationEngine(),

        test_designer=TestDesignerAgent()
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

            "strategy": result["strategy"],

            "test_design": result["test_design"],

            "automation_decisions": result["automation_decisions"],

            "risk_coverage": result["risk_coverage"]
        }
    )