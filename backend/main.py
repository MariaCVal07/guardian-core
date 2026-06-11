#EL CEREBRO DE GUARDIÁN.

from backend.agents.business_analyst.agent import BusinessAnalystAgent
from backend.agents.test_case_generator.agent import TestCaseGeneratorAgent
from backend.agents.execution_agent.agent import ExecutionAgent

from backend.file_manager import FileManager
from backend.run_manager import RunManager
from backend.risk_engine import RiskEngine
from backend.strategy_engine import StrategyEngine

requirement = """
Cuando un usuario realiza un login correcto
debe acceder al inventario principal.
"""

print("\n[1] Analizando requerimiento...\n")

business_agent = BusinessAnalystAgent()

analysis = business_agent.analyze_requirement(
    industry="ecommerce",
    product="SauceDemo",
    module="login",
    business_description="Demo store para pruebas de login",
    requirement=requirement,
    acceptance_criteria="Usuario accede al inventario tras login correcto"
)

print("ANALYSIS:")
print(analysis)
print()
print("Análisis completado.\n")


print("[2] Seleccionando template QA...\n")

from backend.template_selector import TemplateSelector

selector = TemplateSelector()

test_code = selector.select_template(
    requirement
)

print("Template seleccionado.\n")


print("[3] Guardando test...\n")

file_manager = FileManager()

test_path = file_manager.save_test_file(
    "guardian_generated.spec.ts",
    test_code
)

print(f"Test guardado en: {test_path}\n")


print("[4] Ejecutando test...\n")

execution_agent = ExecutionAgent()

execution_result = execution_agent.execute_test()

print("EXECUTION RESULT:")
print(execution_result)
print()

print("Ejecución finalizada.\n")


print("[5] Guardando ejecución...\n")

run_manager = RunManager()

run_id = run_manager.create_run({

    "requirement": requirement,
    "analysis": analysis,
    "generated_test": test_code,
    "execution_result": execution_result
})

print(f"Run guardado: {run_id}\n")


print("=====================================")
print("GUARDIÁN AUTONOMOUS QA REPORT")
print("=====================================\n")

print(f"RUN ID: {run_id}\n")

if execution_result["success"]:

    print("STATUS:")
    print("PASSED\n")

else:

    print("STATUS:")
    print("FAILED\n")

print("=====================================")


risk_engine = RiskEngine()

risk_score = risk_engine.calculate_risk(
    industry="ecommerce",
    module="login",
    requirement=requirement
)

strategy_engine = StrategyEngine()

strategy = strategy_engine.determine_strategy(
    analysis,
    risk_score
)

print("Risk score:")
print(risk_score)
print()

print("Testing strategy:")
print(strategy)
print()