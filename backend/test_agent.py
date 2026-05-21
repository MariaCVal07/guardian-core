# 
from agents.business_analyst.agent import (
    BusinessAnalystAgent
)

agent = BusinessAnalystAgent()

result = agent.analyze_requirement(
    """
    Se implementará pago con tarjeta
    y validación antifraude.
    """
)

print(result)