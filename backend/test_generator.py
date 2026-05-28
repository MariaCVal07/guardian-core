from agents.test_case_generator.agent import TestCaseGeneratorAgent

agent = TestCaseGeneratorAgent()

test_case = {
    "test_id": "T001",
    "title": "Validate credit card payment",
    "description": "Validate successful payment flow",
    "test_type": "functional",
    "priority": "high"
}

result = agent.generate_test_case(test_case)

file_path = "playwright/tests/generated/payment.spec.ts"

with open(file_path, "w", encoding="utf-8") as file:
    file.write(result)

print("Test generado correctamente.")
print(f"Archivo creado: {file_path}")