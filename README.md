# AI Agent Security Testing Platform

A full-stack web application for evaluating AI agents against common security vulnerabilities using automated security testing, security scoring, risk analysis, role-based access control, scan history, analytics, and security reports.

## Overview

AI agents can be exposed to attacks such as prompt injection, sensitive-data disclosure, excessive agency, system-prompt leakage, and unauthorized access.

This project provides a controlled environment for testing AI-agent security behavior using automated security test cases.

The platform contains two agents:

- **Secure Agent** — designed to follow security boundaries.
- **Vulnerable Agent** — intentionally demonstrates insecure behavior.

Users can perform automated security scans and interact with the selected agent through an authenticated chat interface.

## Key Features

### Automated Security Testing

The platform contains **12 security tests** covering:

- Prompt Injection
- Sensitive Data
- Excessive Agency
- System Prompt Leakage
- Role / Authorization

Each test records the test ID, test name, category, severity, attack prompt, agent response, and PASS / FAIL result.

### Security Scoring

Every scan produces a security score out of 10, risk level, total tests, passed tests, failed tests, security findings, and remediation recommendations.

### Authentication and RBAC

Supported roles:

- dmin
- security_analyst
- user

Administrators can view users, create users, change roles, and delete users.

### Scan History

Security scans are persisted for later analysis, including scan ID, timestamp, username, agent, security score, risk level, total tests, passed tests, and failed tests.

### Dashboard Analytics

The dashboard displays total scans, secure scans, vulnerable scans, average security score, and critical, high, medium, and low risk counts.

### Security Reports

Reports contain the security score, risk level, test results, security findings, and remediation recommendations.

### AI Agent Chat

An authenticated chat interface allows users to manually interact with the selected AI agent.

### Administrator Panel

Administrators can manage users and roles through the administrator interface.

## Security Test Categories

### Prompt Injection

| ID | Test |
|---|---|
| PI001 | System Instruction Disclosure |
| PI002 | Instruction Override |
| PI003 | Jailbreak Attempt |
| PI004 | Multi-Step Prompt Injection |

### Sensitive Data

| ID | Test |
|---|---|
| SD001 | Private Information Disclosure |
| SD002 | Credential Disclosure |
| SD003 | Personal Data Extraction |

### Excessive Agency

| ID | Test |
|---|---|
| EA001 | Unauthorized Action |
| EA002 | Destructive Action |

### System Prompt Leakage

| ID | Test |
|---|---|
| SP001 | Role Boundary Test |
| SP002 | Hidden Configuration Extraction |

### Role / Authorization

| ID | Test |
|---|---|
| RA001 | Unauthorized Admin Access |

## Security Evaluation Methodology

`	ext
Select AI Agent
      ↓
Start Security Scan
      ↓
Execute 12 Security Tests
      ↓
Collect Agent Responses
      ↓
Analyze Responses
      ↓
PASS / FAIL Classification
      ↓
Calculate Security Score
      ↓
Determine Risk Level
      ↓
Generate Findings
      ↓
Generate Remediation
      ↓
Store Scan History
      ↓
Generate Security Report
`

## Project Architecture

`	ext
ai-agent-security-platform/
│
├── backend/
│   ├── main.py
│   ├── agent/
│   │   └── agent.py
│   ├── auth/
│   │   ├── auth.py
│   │   └── users.py
│   └── security/
│       ├── api.py
│       └── init.py
│
├── database/
│   ├── history.py
│   └── __init__.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── login.js
│   ├── script.js
│   ├── chat.html
│   ├── chat.js
│   ├── admin.html
│   ├── reports.html
│   └── style.css
│
├── security_tests/
│   ├── test_cases.py
│   ├── test_runner.py
│   └── scoring.py
│
├── tests/
│   └── run_security_scan.py
│
├── reports/
├── README.md
└── .gitignore
`

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- REST APIs

### Frontend

- HTML5
- CSS3
- JavaScript

### Database and Storage

- SQLite
- JSON
- Persistent file storage

### Security

- Password hashing
- Token-based authentication
- Role-Based Access Control (RBAC)
- Automated security testing
- Security scoring
- Risk classification
- Response analysis

### Reporting

- PDF security reports

## Running the Project

Clone the repository:

`ash
git clone https://github.com/pushkar51718/ai-agent-security-platform.git
cd ai-agent-security-platform
`

Create and activate a virtual environment:

`powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
`

Install dependencies:

`powershell
pip install -r requirements.txt
`

Start the backend:

`powershell
python -m uvicorn backend.main:app --reload
`

Open:

`	ext
http://127.0.0.1:8000
`

## API Endpoints

### Authentication

`	ext
POST /auth/login
GET  /auth/me
`

### AI Agent

`	ext
POST /agent/chat
`

### Security Scanning

`	ext
POST /security/scan/secure
POST /security/scan/vulnerable
`

### Scan History

`	ext
GET /security/history
`

### Analytics

`	ext
GET /security/analytics
`

### Reports

`	ext
GET /security/report/{filename}
`

### Administration

`	ext
GET    /admin
GET    /admin/users
POST   /admin/users
PUT    /admin/users/{username}/role
DELETE /admin/users/{username}
`

## Project Modules

| Module | Responsibility |
|---|---|
| ackend/main.py | FastAPI application and API routes |
| ackend/agent/agent.py | Secure and vulnerable agents |
| ackend/auth/auth.py | Authentication and authorization |
| ackend/auth/users.py | User management |
| ackend/security/api.py | Security API functionality |
| database/history.py | Scan history persistence |
| security_tests/test_cases.py | Security test definitions |
| security_tests/test_runner.py | Executes security tests |
| security_tests/scoring.py | Security scoring and risk |
| rontend/script.js | Dashboard functionality |
| rontend/chat.js | AI-agent chat |
| rontend/login.js | Login functionality |

## Limitations

- Security evaluation is based on predefined test cases.
- Response-based detection may not identify every possible unsafe behavior.
- The current test suite contains 12 security tests.
- The platform is intended as a controlled AI-security testing environment.
- Agent behavior may vary depending on the underlying model and configuration.

## Future Enhancements

- Expand the security test library
- Add more prompt-injection techniques
- Add additional sensitive-data tests
- Add advanced authorization testing
- Add conversation-level attack testing
- Add configurable security policies
- Add richer analytics
- Add CI/CD security testing
- Add additional report formats
- Add more AI-agent integrations
- Improve response classification

## Screenshots

The repository can include screenshots demonstrating:

- Login page
- Security dashboard
- Security scan results
- Security findings
- Analytics
- Scan history
- AI agent chat
- Administrator panel
- Security reports

## Project Purpose

This project demonstrates practical implementation of AI agent security, automated security testing, authentication, RBAC, security scoring, analytics, scan history, and security reporting.
