from backend.risk_coverage_engine import RiskCoverageEngine


class GuardianPipeline:

    def __init__(
        self,
        business_agent,
        risk_engine,
        risk_analyst,
        strategy_engine,
        test_design_engine,
        automation_engine,
        test_designer
    ):

        self.business_agent = business_agent
        self.risk_engine = risk_engine
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

        analysis["risk_mitigations"] = self.risk_analyst.analyze_risks(
            analysis
        )

        # Estrategia de pruebas
        strategy = self.strategy_engine.determine_strategy(
            industry=industry,
            product=product,
            module=module,
            business_description=business_description,
            analysis=analysis,
            risk_score=risk_score
        )

        # Casos recomendados
        analysis["recommended_tests"] = self.test_designer.generate_tests(
            industry=industry,
            module=module,
            requirement=requirement,
            acceptance_criteria=acceptance_criteria,
            risks=all_risks
        )

        # Diseño de pruebas
        test_design = self.test_design_engine.generate_test_design(
            analysis
        )

        # Automatización
        automation_decisions = self.automation_engine.evaluate(
            test_design
        )

        # Cobertura de riesgos
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
        