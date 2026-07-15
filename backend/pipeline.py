from backend.risk_coverage_engine import RiskCoverageEngine


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

        analysis = self.business_agent.analyze_requirement(
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

        analysis["risk_mitigations"] = (
            self.risk_analyst.analyze_risks(
                analysis
            )
        )

        # ==========================
        # TEST STRATEGY
        # ==========================

        strategy = self.strategy_engine.determine_strategy(
            industry=industry,
            product=product,
            module=module,
            business_description=business_description,
            analysis=analysis
        )

        # ==========================
        # TEST IDENTIFICATION
        # ==========================

        analysis["recommended_tests"] = self.test_designer.generate_tests(
            analysis=analysis,
            requirement=requirement,
            acceptance_criteria=acceptance_criteria
        )

        # ==========================
        # TEST DESIGN
        # ==========================

        test_design = (
            self.test_design_engine.generate_test_design(
                analysis
            )
        )

        # ==========================
        # AUTOMATION
        # ==========================

        automation_decisions = self.automation_engine.evaluate (
            analysis,
            strategy,
            test_design
        )

        # ==========================
        # RISK COVERAGE
        # ==========================

        risk_coverage = (
            self.risk_coverage_engine.calculate(
                analysis.get(
                    "potential_risks",
                    []
                ),
                test_design
            )
        )

        return {
            "analysis": analysis,
            "strategy": strategy,
            "test_design": test_design,
            "automation_decisions": automation_decisions,
            "risk_coverage": risk_coverage
        }
        