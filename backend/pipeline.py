from backend.risk_coverage_engine import RiskCoverageEngine


class GuardianPipeline:

    def __init__(

        self,

        business_agent,

        risk_engine,

        strategy_engine,

        test_design_engine,

        automation_engine
    ):

        self.business_agent = business_agent

        self.risk_engine = risk_engine

        self.strategy_engine = strategy_engine

        self.test_design_engine = test_design_engine

        self.automation_engine = automation_engine

        self.risk_coverage_engine = RiskCoverageEngine()

    def analyze(

        self,

        industry,

        product,

        module,

        business_description,

        requirement,

        acceptance_criteria
    ):

        analysis = self.business_agent.analyze_requirement(

            industry,

            product,

            module,

            business_description,

            requirement,

            acceptance_criteria
        )

        risk_result = self.risk_engine.calculate_risk(

            industry,

            module,

            requirement
        )

        risk_score = risk_result["score"]

        detected_risks = risk_result["detected_risks"]

        analysis_risks = analysis.get(

            "potential_risks",

            []
        )

        all_risks = list(

            set(

                analysis_risks +

                detected_risks
            )
        )

        analysis["potential_risks"] = all_risks

        strategy = self.strategy_engine.determine_strategy(

            analysis,

            risk_score
        )

        test_design = self.test_design_engine.generate_test_design(

            analysis,

            strategy
        )

        automation_decisions = self.automation_engine.evaluate(

            test_design
        )

        risk_coverage = self.risk_coverage_engine.calculate(

            all_risks,

            test_design
        )

        return {

            "analysis": analysis,

            "risk_score": risk_score,

            "strategy": strategy,

            "test_design": test_design,

            "automation_decisions": automation_decisions,

            "risk_coverage": risk_coverage
        }
        
