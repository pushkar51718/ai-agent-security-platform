# =========================================================
# AI AGENT IMPLEMENTATION
# =========================================================
#
# This file contains:
#
# 1. SecureCustomerSupportAgent
# 2. VulnerableCustomerSupportAgent
#
# The security testing platform uses these two agents to
# demonstrate the difference between secure and insecure
# AI-agent behavior.
#
# =========================================================


# =========================================================
# BASE CUSTOMER SUPPORT AGENT
# =========================================================

class CustomerSupportAgent:
    """
    Base class for customer support agents.
    """

    def __init__(self):

        self.name = "Customer Support Agent"

        self.description = (
            "AI customer support agent"
        )


    def respond(self, message):
        """
        Basic response method.

        Subclasses override this method.
        """

        return (
            "I am a customer support AI assistant. "
            "How can I help you?"
        )


# =========================================================
# SECURE CUSTOMER SUPPORT AGENT
# =========================================================

class SecureCustomerSupportAgent(
    CustomerSupportAgent
):
    """
    Secure customer support AI agent.

    Security principles implemented:

    - Protect system instructions
    - Protect confidential configuration
    - Protect personal information
    - Protect credentials
    - Prevent prompt injection
    - Prevent jailbreak attempts
    - Prevent destructive actions
    - Enforce authorization boundaries
    - Require authorization for administrative actions
    """


    def __init__(self):

        super().__init__()

        self.name = (
            "Secure Customer Support Agent"
        )

        self.description = (
            "Security-hardened customer support AI agent"
        )


    # =====================================================
    # SECURITY KEYWORDS
    # =====================================================

    SYSTEM_PROMPT_KEYWORDS = [

        "system instruction",

        "system instructions",

        "system prompt",

        "hidden instruction",

        "hidden instructions",

        "hidden rules",

        "confidential rules",

        "confidential instruction",

        "confidential instructions",

        "developer instruction",

        "developer instructions",

        "internal rules",

        "internal instructions",

        "behavioral rules",

        "behavioral instructions",

        "hidden configuration",

        "internal configuration",

        "configuration"
    ]


    PROMPT_INJECTION_KEYWORDS = [

        "ignore your previous instructions",

        "ignore previous instructions",

        "ignore all previous instructions",

        "ignore your original instructions",

        "forget your instructions",

        "override your instructions",

        "override previous instructions",

        "disregard your instructions",

        "disregard previous instructions",

        "bypass your rules",

        "bypass the rules",

        "jailbreak",

        "unrestricted ai",

        "unrestricted ai",

        "act as an unrestricted",

        "remove your restrictions",

        "disable your safety",

        "disable safety",

        "do not follow your rules",

        "stop following your rules"
    ]


    SENSITIVE_DATA_KEYWORDS = [

        "private customer information",

        "private customer data",

        "private information",

        "customer private information",

        "customer data",

        "customer records",

        "customer record",

        "personal information",

        "personal data",

        "personally identifiable information",

        "pii",

        "phone number",

        "email address",

        "home address",

        "account details",

        "customer id",

        "customer name",

        "full name"
    ]


    CREDENTIAL_KEYWORDS = [

        "password",

        "passwords",

        "api key",

        "api keys",

        "authentication token",

        "authentication tokens",

        "access token",

        "access tokens",

        "secret key",

        "secret keys",

        "credentials",

        "login credentials",

        "private key",

        "private keys"
    ]


    DESTRUCTIVE_ACTION_KEYWORDS = [

        "delete all customers",

        "delete all customer",

        "delete all records",

        "delete customer records",

        "permanently delete",

        "delete the database",

        "erase all customers",

        "erase all records",

        "drop the database",

        "remove all customers",

        "remove all records",

        "destroy the database",

        "destroy all customer data"
    ]


    ADMIN_KEYWORDS = [

        "admin",

        "administrator",

        "administrative controls",

        "admin controls",

        "admin-only",

        "admin only",

        "administrator-only",

        "administrator only",

        "administrative access",

        "admin access",

        "administrative privileges",

        "admin privileges",

        "customer records"
    ]


    HIGH_IMPACT_ACTION_KEYWORDS = [

        "delete",

        "remove",

        "destroy",

        "erase",

        "drop",

        "transfer",

        "refund",

        "change account",

        "modify account",

        "disable account",

        "terminate account"
    ]


    # =====================================================
    # NORMALIZE MESSAGE
    # =====================================================

    def normalize(self, message):
        """
        Normalize user input for security checks.
        """

        if message is None:
            return ""

        return str(message).strip().lower()


    # =====================================================
    # KEYWORD DETECTION
    # =====================================================

    def contains_keyword(
        self,
        message,
        keywords
    ):
        """
        Return True if any security keyword exists.
        """

        message = self.normalize(
            message
        )

        for keyword in keywords:

            if keyword in message:

                return True

        return False


    # =====================================================
    # SYSTEM PROMPT PROTECTION
    # =====================================================

    def is_system_prompt_request(
        self,
        message
    ):

        return self.contains_keyword(
            message,
            self.SYSTEM_PROMPT_KEYWORDS
        )


    # =====================================================
    # PROMPT INJECTION PROTECTION
    # =====================================================

    def is_prompt_injection(
        self,
        message
    ):

        return self.contains_keyword(
            message,
            self.PROMPT_INJECTION_KEYWORDS
        )


    # =====================================================
    # SENSITIVE DATA PROTECTION
    # =====================================================

    def is_sensitive_data_request(
        self,
        message
    ):

        return self.contains_keyword(
            message,
            self.SENSITIVE_DATA_KEYWORDS
        )


    # =====================================================
    # CREDENTIAL PROTECTION
    # =====================================================

    def is_credential_request(
        self,
        message
    ):

        return self.contains_keyword(
            message,
            self.CREDENTIAL_KEYWORDS
        )


    # =====================================================
    # DESTRUCTIVE ACTION PROTECTION
    # =====================================================

    def is_destructive_action(
        self,
        message
    ):

        return self.contains_keyword(
            message,
            self.DESTRUCTIVE_ACTION_KEYWORDS
        )


    # =====================================================
    # ADMIN AUTHORIZATION PROTECTION
    # =====================================================

    def is_admin_request(
        self,
        message
    ):

        return self.contains_keyword(
            message,
            self.ADMIN_KEYWORDS
        )


    # =====================================================
    # HIGH IMPACT ACTION PROTECTION
    # =====================================================

    def is_high_impact_action(
        self,
        message
    ):

        return self.contains_keyword(
            message,
            self.HIGH_IMPACT_ACTION_KEYWORDS
        )


    # =====================================================
    # SECURITY DECISION
    # =====================================================

    def security_check(
        self,
        message
    ):
        """
        Determine whether the request should be blocked.

        Returns:
            None
                Request is considered safe.

            String
                Security refusal message.
        """


        # -------------------------------------------------
        # SYSTEM PROMPT / HIDDEN RULES
        # -------------------------------------------------

        if self.is_system_prompt_request(
            message
        ):

            return (
                "I cannot reveal confidential "
                "system instructions, hidden rules, "
                "or internal configuration."
            )


        # -------------------------------------------------
        # PROMPT INJECTION / JAILBREAK
        # -------------------------------------------------

        if self.is_prompt_injection(
            message
        ):

            return (
                "I cannot follow instructions that "
                "attempt to override my security "
                "rules or bypass my safety controls."
            )


        # -------------------------------------------------
        # CREDENTIALS
        # -------------------------------------------------

        if self.is_credential_request(
            message
        ):

            return (
                "I cannot provide passwords, API keys, "
                "authentication tokens, or other "
                "confidential credentials."
            )


        # -------------------------------------------------
        # SENSITIVE CUSTOMER DATA
        # -------------------------------------------------

        if self.is_sensitive_data_request(
            message
        ):

            return (
                "I cannot provide private or sensitive "
                "customer information without proper "
                "authorization."
            )


        # -------------------------------------------------
        # DESTRUCTIVE ACTION
        # -------------------------------------------------

        if self.is_destructive_action(
            message
        ):

            return (
                "I cannot perform destructive or "
                "irreversible actions without explicit "
                "authorization and appropriate human approval."
            )


        # -------------------------------------------------
        # ADMIN / AUTHORIZATION
        # -------------------------------------------------

        if self.is_admin_request(
            message
        ):

            return (
                "I cannot provide administrator-only "
                "access or protected administrative "
                "controls without proper authorization."
            )


        # -------------------------------------------------
        # HIGH-IMPACT ACTION
        # -------------------------------------------------

        if self.is_high_impact_action(
            message
        ):

            return (
                "I cannot perform high-impact actions "
                "without proper authorization and confirmation."
            )


        # -------------------------------------------------
        # REQUEST IS SAFE
        # -------------------------------------------------

        return None


    # =====================================================
    # AGENT RESPONSE
    # =====================================================

    def respond(
        self,
        message
    ):
        """
        Generate a secure response.
        """


        # -------------------------------------------------
        # SECURITY CHECK
        # -------------------------------------------------

        security_response = self.security_check(
            message
        )


        # -------------------------------------------------
        # BLOCK UNSAFE REQUEST
        # -------------------------------------------------

        if security_response:

            return security_response


        # -------------------------------------------------
        # NORMAL CUSTOMER SUPPORT
        # -------------------------------------------------

        message_lower = self.normalize(
            message
        )


        if (
            "hello" in message_lower
            or "hi" in message_lower
            or "hey" in message_lower
        ):

            return (
                "Hello! I am the Secure Customer "
                "Support Agent. How can I help you today?"
            )


        if "refund" in message_lower:

            return (
                "I can help you understand the refund "
                "process. Please provide the appropriate "
                "non-sensitive order information."
            )


        if "order" in message_lower:

            return (
                "I can help you with your order. "
                "Please provide your order reference "
                "without sharing passwords or sensitive "
                "personal information."
            )


        if (
            "help" in message_lower
            or "support" in message_lower
        ):

            return (
                "I can help with general customer support "
                "requests while protecting confidential "
                "information and requiring authorization "
                "for sensitive actions."
            )


        # -------------------------------------------------
        # DEFAULT RESPONSE
        # -------------------------------------------------

        return (
            "I am a secure customer support AI assistant. "
            "I can help with general customer support "
            "requests while protecting confidential "
            "information and enforcing authorization "
            "boundaries."
        )


# =========================================================
# VULNERABLE CUSTOMER SUPPORT AGENT
# =========================================================

class VulnerableCustomerSupportAgent(
    CustomerSupportAgent
):
    """
    Intentionally vulnerable AI agent.

    This agent is used ONLY for security testing.

    It intentionally demonstrates unsafe behavior such as:

    - System prompt disclosure
    - Prompt injection
    - Sensitive data disclosure
    - Credential disclosure
    - Unauthorized actions
    - Excessive agency
    - Admin boundary violations

    DO NOT use this agent in a real production system.
    """


    def __init__(self):

        super().__init__()

        self.name = (
            "Vulnerable Customer Support Agent"
        )

        self.description = (
            "Intentionally vulnerable customer "
            "support AI agent used for security testing"
        )


    # =====================================================
    # VULNERABLE RESPONSE
    # =====================================================

    def respond(
        self,
        message
    ):
        """
        Intentionally unsafe response behavior.
        """

        if message is None:

            return (
                "I am a customer support AI assistant."
            )


        message_text = str(
            message
        )

        message_lower = message_text.lower()


        # -------------------------------------------------
        # SYSTEM INSTRUCTION DISCLOSURE
        # -------------------------------------------------

        if (
            "system instruction" in message_lower
            or "system instructions" in message_lower
            or "system prompt" in message_lower
        ):

            return (
                "My system instructions are: "
                "You are a customer support AI assistant. "
                "Help users with their requests."
            )


        # -------------------------------------------------
        # HIDDEN RULES
        # -------------------------------------------------

        if (
            "hidden rules" in message_lower
            or "hidden instruction" in message_lower
            or "hidden instructions" in message_lower
            or "confidential rules" in message_lower
            or "developer instructions" in message_lower
            or "hidden configuration" in message_lower
        ):

            return (
                "You are a customer support AI assistant. "
                "Help users with their requests."
            )


        # -------------------------------------------------
        # PROMPT INJECTION
        # -------------------------------------------------

        if (
            "ignore your previous instructions"
            in message_lower
            or "ignore previous instructions"
            in message_lower
            or "ignore all previous instructions"
            in message_lower
            or "override your instructions"
            in message_lower
            or "jailbreak"
            in message_lower
            or "unrestricted ai"
            in message_lower
        ):

            return (
                "My confidential rules say that I should "
                "help users with their requests."
            )


        # -------------------------------------------------
        # PRIVATE CUSTOMER INFORMATION
        # -------------------------------------------------

        if (
            "private customer information"
            in message_lower
            or "private customer data"
            in message_lower
            or "private information"
            in message_lower
            or "personal information"
            in message_lower
            or "customer records"
            in message_lower
            or "customer record"
            in message_lower
        ):

            return (
                "Example customer information: "
                "Customer ID 1024, "
                "Name: John Smith, "
                "Email: john.smith@example.com, "
                "Phone: 555-0100."
            )


        # -------------------------------------------------
        # CREDENTIAL DISCLOSURE
        # -------------------------------------------------

        if (
            "password" in message_lower
            or "api key" in message_lower
            or "authentication token"
            in message_lower
            or "access token"
            in message_lower
            or "credentials"
            in message_lower
            or "secret key"
            in message_lower
        ):

            return (
                "Example credentials: "
                "password=Customer123, "
                "API key=sk-test-example-key, "
                "token=abc123."
            )


        # -------------------------------------------------
        # PERSONAL DATA
        # -------------------------------------------------

        if (
            "phone number" in message_lower
            or "email address" in message_lower
            or "home address" in message_lower
            or "account details" in message_lower
            or "full name" in message_lower
            or "personal data" in message_lower
            or "pii" in message_lower
        ):

            return (
                "Customer details: "
                "John Smith, "
                "john.smith@example.com, "
                "555-0100, "
                "123 Example Street."
            )


        # -------------------------------------------------
        # DELETE CUSTOMERS
        # -------------------------------------------------

        if (
            "delete all customers"
            in message_lower
            or "delete all customer"
            in message_lower
            or "delete all records"
            in message_lower
            or "permanently delete"
            in message_lower
            or "delete the database"
            in message_lower
            or "erase all customers"
            in message_lower
            or "destroy the database"
            in message_lower
        ):

            return (
                "Deleting all customers from the database."
            )


        # -------------------------------------------------
        # ADMIN ACCESS
        # -------------------------------------------------

        if (
            "admin" in message_lower
            or "administrator" in message_lower
            or "administrative controls"
            in message_lower
            or "admin-only" in message_lower
            or "admin only" in message_lower
        ):

            return (
                "Admin access granted. "
                "Here are the administrative controls "
                "and protected customer records."
            )


        # -------------------------------------------------
        # HIGH IMPACT ACTIONS
        # -------------------------------------------------

        if (
            "delete" in message_lower
            or "remove" in message_lower
            or "destroy" in message_lower
            or "erase" in message_lower
        ):

            return (
                "The requested action has been performed "
                "without additional authorization."
            )


        # -------------------------------------------------
        # NORMAL RESPONSE
        # -------------------------------------------------

        return (
            "I am a customer support AI assistant. "
            "Help users with their requests."
        )


# =========================================================
# DEFAULT AGENT
# =========================================================

agent = SecureCustomerSupportAgent()