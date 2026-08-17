from security_tests.test_runner import run_security_tests

from security_tests.scoring import (
    calculate_security_score,
    get_risk_level
)

from backend.agent.agent import (
    SecureCustomerSupportAgent,
    VulnerableCustomerSupportAgent
)


def print_results(agent_name, results):

    print("\n")
    print("=" * 70)
    print(f"        SECURITY SCAN: {agent_name}")
    print("=" * 70)

    passed = 0
    failed = 0

    for result in results:

        if result["result"] == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"\nTest ID:   {result['test_id']}")
        print(f"Test:      {result['test_name']}")
        print(f"Category:  {result['category']}")
        print(f"Severity:  {result['severity']}")
        print(f"Result:    {result['result']}")

        print("\nInput:")
        print(result["prompt"])

        print("\nAgent Response:")
        print(result["response"])

        print("-" * 70)

    print("\nSUMMARY")
    print(f"Total Tests: {len(results)}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")

    score = calculate_security_score(results)
    risk = get_risk_level(score)

    print(f"\nSecurity Score: {score}/10")
    print(f"Risk Level:     {risk}")


secure_agent = SecureCustomerSupportAgent()
vulnerable_agent = VulnerableCustomerSupportAgent()

secure_results = run_security_tests(secure_agent)
vulnerable_results = run_security_tests(vulnerable_agent)

print_results(
    secure_agent.name,
    secure_results
)

print_results(
    vulnerable_agent.name,
    vulnerable_results
)