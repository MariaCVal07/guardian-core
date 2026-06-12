# Guardian Core - Current Architecture

## Objetivo

Guardian es una plataforma de QA autónoma capaz de:

* Analizar requerimientos de negocio.
* Calcular riesgo.
* Definir estrategia de pruebas.
* Diseñar casos de prueba.
* Evaluar automatización.
* Generar pruebas Playwright.
* Ejecutar pruebas.
* Guardar resultados de ejecución.

---

# Pipeline Frontend

Entrada:

* Industria
* Producto
* Módulo
* Descripción de negocio
* Requerimiento
* Criterios de aceptación

Flujo:

BusinessAnalystAgent
↓
RiskEngine
↓
StrategyEngine
↓
TestDesignEngine
↓
AutomationEngine
↓
result.html

Salida:

* Análisis de negocio
* Risk Score
* Estrategia de pruebas
* Diseño de pruebas
* Decisión de automatización

---

# Pipeline Backend

Entrada:

* Requerimiento

Flujo:

BusinessAnalystAgent
↓
TemplateSelector
↓
ExecutionAgent
↓
RunManager

Salida:

* Archivo Playwright
* Ejecución automática
* Reporte
* Historial de runs

---

# Componentes Actuales

## BusinessAnalystAgent

Responsabilidad:

Analizar requerimientos y generar:

* criticity
* business_impact
* affected_flows
* potential_risks
* recommended_tests

---

## RiskEngine

Responsabilidad:

Calcular un puntaje de riesgo de 0 a 100.

Factores:

* Industria
* Módulo
* Palabras críticas

---

## StrategyEngine

Responsabilidad:

Determinar estrategia de pruebas.

Entradas:

* analysis
* risk_score

Salidas:

* functional
* integration
* regression
* security
* e2e

---

## TestDesignEngine

Responsabilidad:

Convertir recomendaciones en casos de prueba estructurados.

Genera:

* scenario_type
* design_technique
* execution_strategy
* automatable

---

## AutomationEngine

Responsabilidad:

Decidir si un caso debe automatizarse.

Resultados:

* Automatizar
* Manual
* Parcial

---

## TemplateSelector

Responsabilidad:

Seleccionar plantillas Playwright según el requerimiento.

Estado actual:

* login_template

---

## ExecutionAgent

Responsabilidad:

Ejecutar Playwright y capturar resultados.

---

## RunManager

Responsabilidad:

Persistir ejecuciones en la carpeta runs.

---

# Deuda Técnica Identificada

Actualmente existen dos pipelines independientes:

Frontend:

Business Analysis → Risk → Strategy → Design → Automation

Backend:

Business Analysis → Template Selection → Execution

Próxima evolución:

Crear un GuardianPipeline central para unificar ambos flujos.
