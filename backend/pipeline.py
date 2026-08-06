from backend.engines.risk_coverage_engine import RiskCoverageEngine

class GuardianPipeline:

    def __init__(
        self,
        business_agent,
        risk_analyst,
        strategy_engine,
        test_design_engine,
        automation_engine,
        test_designer
    ):

        self.business_agent = business_agent

        # Se mantiene por compatibilidad.
        # Ya no se utiliza en el MVP.

        self.risk_analyst = risk_analyst
        self.strategy_engine = strategy_engine
        self.test_designer = test_designer
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

        # ==========================
        # BUSINESS ANALYSIS
        # ==========================

        business_analysis = self.business_agent.analyze_requirement(
            industry,
            product,
            module,
            business_description,
            requirement,
            acceptance_criteria
        )

        # ==========================
        # RISK ANALYSIS
        # ==========================

        risk_analysis = self.risk_analyst.analyze_risks(
            business_analysis
        )

        # ==========================
        # TEST STRATEGY
        # ==========================

        strategy = self.strategy_engine.determine_strategy(
            business_model=business_analysis,
            risk_model=risk_analysis
        )

        # ==========================
        # TEST IDENTIFICATION
        # ==========================

        recommended_tests = self.test_designer.generate_tests(
            business_model=business_analysis,
            risk_model=risk_analysis,
            strategy=strategy
        )

        business_analysis["recommended_tests"] = recommended_tests

        # ==========================
        # TEST DESIGN
        # ==========================

        test_design = self.test_design_engine.generate_test_design(
            business_analysis
        )

        # ==========================
        # AUTOMATION
        # ==========================

        automation_decisions = self.automation_engine.evaluate(
            business_analysis,
            strategy,
            test_design
        )

        # ==========================
        # RISK COVERAGE
        # ==========================

        risk_coverage = self.risk_coverage_engine.calculate(
            risk_analysis["identified_risks"],
            test_design
        )

        return {
            "business_analysis": business_analysis,
            "risk_analysis": risk_analysis,
            "strategy": strategy,
            "recommended_tests": recommended_tests,
            "test_design": test_design,
            "automation_decisions": automation_decisions,
            "risk_coverage": risk_coverage
        }
            