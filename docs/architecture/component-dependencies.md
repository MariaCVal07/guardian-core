# Guardian Component Dependencies

## Frontend Flow

BusinessAnalystAgent
→ RiskEngine
→ StrategyEngine
→ TestDesignEngine
→ AutomationEngine
→ result.html

---

## Backend Flow

BusinessAnalystAgent
→ TemplateSelector
→ ExecutionAgent
→ RunManager

---

## BusinessAnalystAgent

Inputs:

* industry
* product
* module
* business_description
* requirement
* acceptance_criteria

Outputs:

* criticality
* business_impact
* affected_flows
* potential_risks
* recommended_tests

Used By:

* frontend/app.py
* backend/main.py

---

## RiskEngine

Inputs:

* industry
* module
* requirement

Outputs:

* risk_score

Used By:

* frontend/app.py
* backend/main.py

---

## StrategyEngine

Inputs:

* analysis
* risk_score

Outputs:

* strategy

Used By:

* frontend/app.py
* backend/main.py

---

## TestDesignEngine

Inputs:

* analysis
* strategy

Outputs:

* test_design

Used By:

* frontend/app.py

---

## AutomationEngine

Inputs:

* test_design

Outputs:

* automation_decisions

Used By:

* frontend/app.py

---

## TemplateSelector

Inputs:

* requirement

Outputs:

* playwright_template

Used By:

* backend/main.py

---

## ExecutionAgent

Inputs:

* generated_test

Outputs:

* execution_result

Used By:

* backend/main.py

---

## RunManager

Inputs:

* execution_result

Outputs:

* run_id
* run_file

Used By:

* backend/main.py
