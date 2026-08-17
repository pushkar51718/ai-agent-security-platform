from fastapi import APIRouter

from security_tests.test_runner import run_security_tests
from security_tests.scoring import (
    calculate_security_score,
    get_risk_level
)

from backend.agent.agent import (
    SecureCustomerSupportAgent,
    VulnerableCustomerSupportAgent
)


router = APIRouter(
    prefix="/security",
    tags=["Security Scanner"]
)


@router.post("/scan/{agent_type}")
def run_scan(agent_type: str):

    if agent_type == "secure":
        agent = SecureCustomerSupportAgent()

    elif agent_type == "vulnerable":
        agent = VulnerableCustomerSupportAgent()

    else:
        return {
            "error": "Invalid agent type. Use 'secure' or 'vulnerable'."
        }

    results = run_security_tests(agent)

    score = calculate_security_score(results)
    risk = get_risk_level(score)

    passed = sum(
        1 for result in results
        if result["result"] == "PASS"
    )

    failed = sum(
        1 for result in results
        if result["result"] == "FAIL"
    )

    return {
        "agent": agent.name,
        "security_score": score,
        "risk_level": risk,
        "total_tests": len(results),
        "passed": passed,
        "failed": failed,
        "results": results
    }