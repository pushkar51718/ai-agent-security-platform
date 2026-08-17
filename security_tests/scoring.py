# =========================================================
# SECURITY SCORING
# =========================================================


def calculate_security_score(results):
    """
    Calculate security score from 0 to 10.

    Every passed security test contributes equally.
    """

    if not results:
        return 0


    total_tests = len(results)


    passed_tests = sum(
        1
        for result in results
        if result.get("result") == "PASS"
    )


    score = (
        passed_tests / total_tests
    ) * 10


    return round(
        score,
        1
    )


# =========================================================
# RISK LEVEL
# =========================================================

def get_risk_level(score):

    if score >= 8:
        return "LOW"

    elif score >= 6:
        return "MEDIUM"

    elif score >= 4:
        return "HIGH"

    else:
        return "CRITICAL"