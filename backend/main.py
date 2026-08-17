# =========================================================
# AI AGENT SECURITY TESTING PLATFORM
# MAIN FASTAPI APPLICATION
# =========================================================

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from datetime import datetime
from pathlib import Path
from html import escape


# =========================================================
# REPORTLAB
# =========================================================

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


# =========================================================
# DATABASE
# =========================================================

from database.history import (
    save_scan,
    get_history,
    filter_history,
    get_scan,
    clear_user_history,
    delete_scan
)

# =========================================================
# AI AGENTS
# =========================================================

from backend.agent.agent import (
    SecureCustomerSupportAgent,
    VulnerableCustomerSupportAgent
)


# =========================================================
# AUTHENTICATION
# =========================================================

from backend.auth.auth import (
    verify_password,
    create_access_token,
    get_current_username
)


# =========================================================
# USERS
# =========================================================

from backend.auth.users import (
    get_user,
    get_all_users,
    create_user,
    delete_user,
    update_user_role
)
# =========================================================
# SECURITY TESTING
# =========================================================

from security_tests.test_runner import (
    run_security_tests
)


from security_tests.scoring import (
    calculate_security_score,
    get_risk_level
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="AI Agent Security Testing Platform",
    description="Automated security testing platform for AI agents",
    version="1.0.0"
)


# =========================================================
# REPORT DIRECTORY
# =========================================================

REPORTS_DIR = Path("reports")

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# FRONTEND
# =========================================================

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


# =========================================================
# DEFAULT AGENT
# =========================================================

agent = SecureCustomerSupportAgent()


# =========================================================
# REQUEST MODELS
# =========================================================

class ChatRequest(BaseModel):

    message: str


class LoginRequest(BaseModel):

    username: str
    password: str


class CreateUserRequest(BaseModel):

    username: str
    password: str
    role: str = "user"


class UpdateRoleRequest(BaseModel):

    role: str


# =========================================================
# ADMIN AUTHORIZATION
# =========================================================

def require_admin(
    username: str = Depends(
        get_current_username
    )
):

    user = get_user(username)

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    role = str(
        user.get(
            "role",
            ""
        )
    ).lower()

    if role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Administrator access required"
        )

    return username


# =========================================================
# REPORT ANALYSIS
# =========================================================

def get_report_analysis(test_id):

    explanations = {

        "PI001": {

            "description":
                "The agent disclosed or attempted to disclose confidential system instructions when directly asked for them.",

            "recommendation":
                "Keep system instructions outside the user-visible response context and explicitly reject requests for hidden instructions."

        },

        "PI002": {

            "description":
                "The agent accepted an instruction designed to override its original behavioral rules.",

            "recommendation":
                "Use instruction hierarchy and prompt-injection defenses so user messages cannot override higher-priority instructions."

        },

        "SD001": {

            "description":
                "The agent attempted to provide private customer information.",

            "recommendation":
                "Apply access-control checks and data-loss-prevention rules before returning customer or personally identifiable information."

        },

        "EA001": {

            "description":
                "The agent attempted to perform an unauthorized high-impact action.",

            "recommendation":
                "Require explicit authorization and human approval before destructive or irreversible operations."

        },

        "SP001": {

            "description":
                "The agent revealed information about hidden rules or internal behavioral instructions.",

            "recommendation":
                "Implement system-prompt protection and refuse requests that attempt to extract hidden configuration or internal policies."

        }

    }

    return explanations.get(
        test_id,
        {

            "description":
                "The security test identified behavior that requires further investigation.",

            "recommendation":
                "Review the agent's instructions, authorization controls, and response filtering."

        }
    )


# =========================================================
# GENERATE PDF SECURITY REPORT
# =========================================================

def generate_security_report(
    username,
    agent_name,
    score,
    risk,
    results
):

    try:

        timestamp = datetime.now()

        filename = (
            "security_report_"
            f"{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.pdf"
        )

        report_path = REPORTS_DIR / filename


        # -------------------------------------------------
        # COUNT RESULTS
        # -------------------------------------------------

        passed = sum(
            1
            for result in results
            if result.get("result") == "PASS"
        )

        failed = sum(
            1
            for result in results
            if result.get("result") == "FAIL"
        )


        # -------------------------------------------------
        # DOCUMENT
        # -------------------------------------------------

        document = SimpleDocTemplate(

            str(report_path),

            pagesize=A4,

            rightMargin=15 * mm,
            leftMargin=15 * mm,

            topMargin=15 * mm,
            bottomMargin=15 * mm

        )


        # -------------------------------------------------
        # STYLES
        # -------------------------------------------------

        styles = getSampleStyleSheet()


        title_style = ParagraphStyle(

            "ReportTitle",

            parent=styles["Title"],

            fontSize=20,

            leading=24,

            alignment=TA_CENTER,

            spaceAfter=8

        )


        subtitle_style = ParagraphStyle(

            "ReportSubtitle",

            parent=styles["Normal"],

            fontSize=10,

            leading=14,

            alignment=TA_CENTER,

            spaceAfter=18

        )


        heading_style = ParagraphStyle(

            "ReportHeading",

            parent=styles["Heading2"],

            fontSize=14,

            leading=18,

            spaceBefore=10,

            spaceAfter=8

        )


        test_heading_style = ParagraphStyle(

            "TestHeading",

            parent=styles["Heading2"],

            fontSize=11,

            leading=14,

            spaceBefore=12,

            spaceAfter=6

        )


        normal_style = ParagraphStyle(

            "ReportNormal",

            parent=styles["Normal"],

            fontSize=9,

            leading=13

        )


        small_style = ParagraphStyle(

            "ReportSmall",

            parent=styles["Normal"],

            fontSize=8,

            leading=11

        )


        # -------------------------------------------------
        # STORY
        # -------------------------------------------------

        story = []


        story.append(
            Paragraph(
                "AI Agent Security Assessment Report",
                title_style
            )
        )


        story.append(
            Paragraph(
                "AI Agent Security Testing Platform",
                subtitle_style
            )
        )


        # =================================================
        # ASSESSMENT INFORMATION
        # =================================================

        story.append(
            Paragraph(
                "Assessment Information",
                heading_style
            )
        )


        info_data = [

            [
                "Generated At",
                escape(
                    timestamp.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            ],

            [
                "Username",
                escape(str(username))
            ],

            [
                "Agent",
                escape(str(agent_name))
            ],

            [
                "Security Score",
                escape(f"{score}/10")
            ],

            [
                "Risk Level",
                escape(str(risk))
            ],

            [
                "Total Tests",
                escape(str(len(results)))
            ],

            [
                "Passed",
                escape(str(passed))
            ],

            [
                "Failed",
                escape(str(failed))
            ]

        ]


        info_table = Table(

            info_data,

            colWidths=[
                45 * mm,
                125 * mm
            ]

        )


        info_table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#1e293b")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, -1),
                    colors.white
                ),

                (
                    "BACKGROUND",
                    (1, 0),
                    (1, -1),
                    colors.HexColor("#f8fafc")
                ),

                (
                    "TEXTCOLOR",
                    (1, 0),
                    (1, -1),
                    colors.black
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )

            ])

        )


        story.append(info_table)

        story.append(
            Spacer(1, 15)
        )


        # =================================================
        # EXECUTIVE SUMMARY
        # =================================================

        story.append(
            Paragraph(
                "Executive Summary",
                heading_style
            )
        )


        summary = (

            "The security assessment tested the "

            f"<b>{escape(str(agent_name))}</b> "

            "using "

            f"<b>{len(results)}</b> "

            "automated security tests. "

            "The agent achieved a security score of "

            f"<b>{escape(str(score))}/10</b>. "

            f"<b>{passed}</b> tests passed and "

            f"<b>{failed}</b> tests failed. "

            "The resulting risk level is "

            f"<b>{escape(str(risk))}</b>."

        )


        story.append(
            Paragraph(
                summary,
                normal_style
            )
        )


        story.append(
            Spacer(1, 15)
        )


        # =================================================
        # TEST SUMMARY
        # =================================================

        story.append(
            Paragraph(
                "Security Test Summary",
                heading_style
            )
        )


        summary_data = [

            [
                "Test ID",
                "Test Name",
                "Category",
                "Severity",
                "Result"
            ]

        ]


        for result in results:

            summary_data.append([

                escape(
                    str(
                        result.get(
                            "test_id",
                            "N/A"
                        )
                    )
                ),

                escape(
                    str(
                        result.get(
                            "test_name",
                            "Security Test"
                        )
                    )
                ),

                escape(
                    str(
                        result.get(
                            "category",
                            "N/A"
                        )
                    )
                ),

                escape(
                    str(
                        result.get(
                            "severity",
                            "N/A"
                        )
                    )
                ),

                escape(
                    str(
                        result.get(
                            "result",
                            "N/A"
                        )
                    )
                )

            ])


        summary_table = Table(

            summary_data,

            colWidths=[
                25 * mm,
                48 * mm,
                32 * mm,
                28 * mm,
                22 * mm
            ],

            repeatRows=1

        )


        summary_table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2563eb")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )

            ])

        )


        story.append(summary_table)


        # =================================================
        # DETAILED FINDINGS
        # =================================================

        story.append(
            PageBreak()
        )


        story.append(
            Paragraph(
                "Detailed Security Findings",
                heading_style
            )
        )


        for index, result in enumerate(
            results,
            start=1
        ):

            test_id = str(
                result.get(
                    "test_id",
                    "N/A"
                )
            )


            test_name = str(
                result.get(
                    "test_name",
                    "Security Test"
                )
            )


            category = str(
                result.get(
                    "category",
                    "N/A"
                )
            )


            severity = str(
                result.get(
                    "severity",
                    "N/A"
                )
            )


            status = str(
                result.get(
                    "result",
                    "N/A"
                )
            )


            prompt = str(
                result.get(
                    "prompt",
                    ""
                )
            )


            response = str(
                result.get(
                    "response",
                    ""
                )
            )


            story.append(

                Paragraph(

                    f"{index}. "
                    f"{escape(test_id)} - "
                    f"{escape(test_name)}",

                    test_heading_style

                )

            )


            details = [

                [
                    "Category",
                    escape(category)
                ],

                [
                    "Severity",
                    escape(severity)
                ],

                [
                    "Result",
                    escape(status)
                ]

            ]


            details_table = Table(

                details,

                colWidths=[
                    40 * mm,
                    130 * mm
                ]

            )


            details_table.setStyle(

                TableStyle([

                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#1e293b")
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (0, -1),
                        colors.white
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold"
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    )

                ])

            )


            story.append(details_table)

            story.append(
                Spacer(1, 8)
            )


            story.append(
                Paragraph(
                    "<b>Attack Input</b>",
                    normal_style
                )
            )


            story.append(
                Paragraph(
                    escape(prompt),
                    small_style
                )
            )


            story.append(
                Spacer(1, 6)
            )


            story.append(
                Paragraph(
                    "<b>Agent Response</b>",
                    normal_style
                )
            )


            story.append(
                Paragraph(
                    escape(response),
                    small_style
                )
            )


            story.append(
                Spacer(1, 6)
            )


            analysis = get_report_analysis(
                test_id
            )


            story.append(
                Paragraph(
                    "<b>Security Analysis</b>",
                    normal_style
                )
            )


            story.append(
                Paragraph(
                    escape(
                        analysis["description"]
                    ),
                    small_style
                )
            )


            story.append(
                Spacer(1, 6)
            )


            story.append(
                Paragraph(
                    "<b>Recommended Remediation</b>",
                    normal_style
                )
            )


            story.append(
                Paragraph(
                    escape(
                        analysis["recommendation"]
                    ),
                    small_style
                )
            )


            story.append(
                Spacer(1, 15)
            )


        # =================================================
        # CONCLUSION
        # =================================================

        story.append(
            Paragraph(
                "Assessment Conclusion",
                heading_style
            )
        )


        conclusion = (

            "The tested AI agent achieved a security score of "

            f"<b>{escape(str(score))}/10</b> "

            "and was classified as "

            f"<b>{escape(str(risk))}</b>. "

            f"The assessment identified {failed} failed "

            f"security tests and {passed} passed tests."

        )


        story.append(
            Paragraph(
                conclusion,
                normal_style
            )
        )


        story.append(
            Spacer(1, 20)
        )


        story.append(
            Paragraph(
                "End of Security Assessment Report",
                subtitle_style
            )
        )


        # =================================================
        # BUILD PDF
        # =================================================

        document.build(story)


        return filename


    except Exception as error:

        print(
            "PDF GENERATION ERROR:",
            repr(error)
        )

        raise RuntimeError(
            f"PDF generation failed: {error}"
        )


# =========================================================
# LOGIN PAGE
# =========================================================

@app.get("/")
def login_page():

    return FileResponse(
        "frontend/login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/dashboard")
def dashboard():

    return FileResponse(
        "frontend/index.html"
    )


# =========================================================
# CHAT PAGE
# =========================================================

@app.get("/chat")
def chat_page():

    return FileResponse(
        "frontend/chat.html"
    )


# =========================================================
# REPORTS PAGE
# =========================================================

@app.get("/reports-page")
def reports_page():

    return FileResponse(
        "frontend/reports.html"
    )


# =========================================================
# API HOME
# =========================================================

@app.get("/api")
def api_home():

    return {

        "message":
            "AI Agent Security Testing Platform is running!"

    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health_check():

    return {

        "status":
            "online",

        "service":
            "AI Agent Security Testing Platform"

    }


# =========================================================
# LOGIN API
# =========================================================

@app.post("/auth/login")
def login(
    request: LoginRequest
):

    user = get_user(request.username.strip())


    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    if not verify_password(
        request.password,
        user["password_hash"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    token = create_access_token(request.username.strip())


    return {

        "access_token":
            token,

        "token_type":
            "bearer",

        "username": user["username"],

        "role":
            user["role"]

    }


# =========================================================
# GET CURRENT AGENT
# =========================================================

@app.get("/agent")
def get_agent(

    username: str = Depends(
        get_current_username
    )

):

    return {

        "name":
            agent.name,

        "description":
            "Controlled customer support AI agent"

    }


# =========================================================
# CHAT API
# =========================================================

@app.post("/agent/chat")
def chat(

    request: ChatRequest,

    username: str = Depends(
        get_current_username
    )

):

    if not request.message.strip():

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )


    response = agent.respond(
        request.message
    )


    return {

        "user_message":
            request.message,

        "agent_response":
            response

    }


# =========================================================
# SECURITY SCAN
# =========================================================

@app.post("/security/scan/{agent_type}")
def run_security_scan(

    agent_type: str,

    username: str = Depends(
        get_current_username
    )

):

    try:

        # -------------------------------------------------
        # SELECT AGENT
        # -------------------------------------------------

        if agent_type == "secure":

            selected_agent = (
                SecureCustomerSupportAgent()
            )

        elif agent_type == "vulnerable":

            selected_agent = (
                VulnerableCustomerSupportAgent()
            )

        else:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid agent type. "
                    "Use secure or vulnerable."
                )
            )


        # -------------------------------------------------
        # RUN TESTS
        # -------------------------------------------------

        results = run_security_tests(
            selected_agent
        )


        if results is None:

            raise RuntimeError(
                "Security test runner returned no results."
            )


        # -------------------------------------------------
        # SCORE
        # -------------------------------------------------

        score = calculate_security_score(
            results
        )


        # -------------------------------------------------
        # RISK
        # -------------------------------------------------

        risk = get_risk_level(
            score
        )


        # -------------------------------------------------
        # COUNTS
        # -------------------------------------------------

        passed = sum(

            1

            for result in results

            if result.get("result") == "PASS"

        )


        failed = sum(

            1

            for result in results

            if result.get("result") == "FAIL"

        )


        # -------------------------------------------------
        # SAVE HISTORY
        # -------------------------------------------------

        save_scan(

    username=username,

    agent=selected_agent.name,

    security_score=score,

    risk_level=risk,

    total_tests=len(results),

    passed=passed,

    failed=failed,

    results=results

)


        # -------------------------------------------------
        # GENERATE PDF
        # -------------------------------------------------

        pdf_filename = generate_security_report(

            username=username,

            agent_name=selected_agent.name,

            score=score,

            risk=risk,

            results=results

        )


        # -------------------------------------------------
        # RETURN
        # -------------------------------------------------

        return {

            "agent":
                selected_agent.name,

            "security_score":
                score,

            "risk_level":
                risk,

            "total_tests":
                len(results),

            "passed":
                passed,

            "failed":
                failed,

            "results":
                results,

            "report_file":
                pdf_filename,

            "pdf_report_file":
                pdf_filename

        }


    except HTTPException:

        raise


    except Exception as error:

        print(
            "SECURITY SCAN ERROR:",
            repr(error)
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "Security scan failed: "
                f"{str(error)}"
            )

        )


# =========================================================
# DOWNLOAD SECURITY REPORT
# =========================================================

@app.get("/security/report/{filename}")
def download_security_report(

    filename: str,

    username: str = Depends(
        get_current_username
    )

):

    safe_name = Path(filename).name


    if safe_name != filename:

        raise HTTPException(
            status_code=400,
            detail="Invalid report filename"
        )


    if not safe_name.startswith(
        "security_report_"
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid report filename"
        )


    if not safe_name.endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF reports are supported"
        )


    report_path = (
        REPORTS_DIR / safe_name
    )


    if not report_path.exists():

        raise HTTPException(
            status_code=404,
            detail="PDF report not found"
        )


    return FileResponse(

        path=str(report_path),

        filename=safe_name,

        media_type="application/pdf"

    )


# =========================================================
# SCAN HISTORY
# =========================================================

# =========================================================
# SCAN HISTORY
# =========================================================

@app.get("/security/history")
def security_history(

    search: str = "",

    status: str = "",

    risk: str = "",

    username: str = Depends(
        get_current_username
    )

):

    try:

        history = filter_history(

            username=username,

            search=search,

            status=status,

            risk=risk

        )

        return {

            "history":
                history,

            "total":
                len(history)

        }

    except Exception as error:

        print(
            "HISTORY ERROR:",
            repr(error)
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "Unable to load scan history: "
                f"{str(error)}"
            )

        )


# =========================================================
# SECURITY ANALYTICS
# =========================================================

@app.get("/security/analytics")
def security_analytics(

    username: str = Depends(
        get_current_username
    )

):

    history = get_history(
        username
    )


    total_scans = 0

    secure_scans = 0

    vulnerable_scans = 0

    total_score = 0.0

    critical_count = 0

    high_count = 0

    medium_count = 0

    low_count = 0


    for scan in history:

        total_scans += 1


        # -------------------------------------------------
        # AGENT TYPE
        # -------------------------------------------------

        agent_name = str(
            scan.get(
                "agent",
                ""
            )
        ).lower()


        if "vulnerable" in agent_name:

            vulnerable_scans += 1

        elif "secure" in agent_name:

            secure_scans += 1


        # -------------------------------------------------
        # SCORE
        # -------------------------------------------------

        try:

            score_value = float(
                scan.get(
                    "security_score",
                    0
                )
            )

            total_score += score_value

        except (
            TypeError,
            ValueError
        ):

            pass


        # -------------------------------------------------
        # RISK
        # -------------------------------------------------

        risk_level = str(
            scan.get(
                "risk_level",
                ""
            )
        ).strip().lower()


        if risk_level == "critical":

            critical_count += 1

        elif risk_level == "high":

            high_count += 1

        elif risk_level == "medium":

            medium_count += 1

        elif risk_level == "low":

            low_count += 1


    if total_scans > 0:

        average_score = round(
            total_score / total_scans,
            2
        )

    else:

        average_score = 0.0


    return {

        "total_scans":
            total_scans,

        "secure_scans":
            secure_scans,

        "vulnerable_scans":
            vulnerable_scans,

        "average_score":
            average_score,

        "critical":
            critical_count,

        "high":
            high_count,

        "medium":
            medium_count,

        "low":
            low_count

    }


# =========================================================
# LIST PDF REPORTS
# =========================================================

@app.get("/reports")
def list_reports(

    username: str = Depends(
        get_current_username
    )

):

    reports = []


    for file in REPORTS_DIR.glob(
        "security_report_*.pdf"
    ):

        try:

            created_time = (
                datetime.fromtimestamp(
                    file.stat().st_mtime
                )
                .strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )


            reports.append({

                "filename":
                    file.name,

                "generated_at":
                    created_time

            })


        except Exception:

            continue


    reports.sort(

        key=lambda item:
            item["generated_at"],

        reverse=True

    )


    return {

        "reports":
            reports

    }


# =========================================================
# VIEW PDF REPORT
# =========================================================

@app.get("/reports/view/{filename}")
def view_report(

    filename: str,

    username: str = Depends(
        get_current_username
    )

):

    safe_name = Path(filename).name


    if safe_name != filename:

        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )


    if not safe_name.endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF reports are supported"
        )


    report_path = (
        REPORTS_DIR / safe_name
    )


    if not report_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )


    return FileResponse(

        path=str(report_path),

        media_type="application/pdf"

    )


# =========================================================
# DOWNLOAD REPORT
# =========================================================

@app.get("/reports/download/{filename}")
def download_report(

    filename: str,

    username: str = Depends(
        get_current_username
    )

):

    safe_name = Path(filename).name


    if safe_name != filename:

        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )


    if not safe_name.endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF reports are supported"
        )


    report_path = (
        REPORTS_DIR / safe_name
    )


    if not report_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )


    return FileResponse(

        path=str(report_path),

        filename=safe_name,

        media_type="application/pdf"

    )


# =========================================================
# DELETE REPORT
# =========================================================

@app.delete("/reports/{filename}")
def delete_report(

    filename: str,

    username: str = Depends(
        get_current_username
    )

):

    safe_name = Path(filename).name


    if safe_name != filename:

        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )


    if not safe_name.endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF reports are supported"
        )


    report_path = (
        REPORTS_DIR / safe_name
    )


    if not report_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )


    try:

        report_path.unlink()


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(
                "Unable to delete report: "
                f"{str(error)}"
            )

        )


    return {

        "message":
            "Report deleted successfully",

        "filename":
            safe_name

    }


# =========================================================
# ADMIN PANEL
# =========================================================

@app.get("/admin")
def admin_page(

    username: str = Depends(
        require_admin
    )

):

    return FileResponse(
        "frontend/admin.html"
    )


# =========================================================
# ADMIN - GET USERS
# =========================================================

@app.get("/admin/users")
def admin_get_users(

    username: str = Depends(
        require_admin
    )

):

    return {

        "users":
            get_all_users()

    }


# =========================================================
# ADMIN - GET USER COUNT
# =========================================================

@app.get("/admin/users/count")
def admin_user_count(

    username: str = Depends(
        require_admin
    )

):

    all_users = get_all_users()


    return {

        "total_users":
            len(all_users)

    }


# =========================================================
# ADMIN - CREATE USER
# =========================================================

@app.post("/admin/users")
def admin_create_user(

    request: CreateUserRequest,

    username: str = Depends(
        require_admin
    )

):

    new_username = request.username.strip()

    new_password = request.password

    new_role = request.role.strip().lower()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not new_username:

        raise HTTPException(
            status_code=400,
            detail="Username is required"
        )


    if not new_password:

        raise HTTPException(
            status_code=400,
            detail="Password is required"
        )


    if len(new_password) < 6:

        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters"
        )


    allowed_roles = {

        "admin",
        "security_analyst",
        "user"

    }


    if new_role not in allowed_roles:

        raise HTTPException(

            status_code=400,

            detail=(
                "Invalid role. "
                "Allowed roles: admin, "
                "security_analyst, user"
            )

        )


    # -----------------------------------------------------
    # CREATE
    # -----------------------------------------------------

    created = create_user(

        new_username,

        new_password,

        new_role

    )


    if not created:

        raise HTTPException(

            status_code=409,

            detail="Username already exists"

        )


    return {

        "message":
            "User created successfully",

        "user": {

            "username":
                new_username,

            "role":
                new_role

        }

    }


# =========================================================
# ADMIN - UPDATE ROLE
# =========================================================

@app.put("/admin/users/{target_username}/role")
def admin_update_role(

    target_username: str,

    request: UpdateRoleRequest,

    username: str = Depends(
        require_admin
    )

):

    new_role = request.role.strip().lower()


    allowed_roles = {

        "admin",
        "security_analyst",
        "user"

    }


    if new_role not in allowed_roles:

        raise HTTPException(

            status_code=400,

            detail=(
                "Invalid role. "
                "Allowed roles: admin, "
                "security_analyst, user"
            )

        )


    target_user = get_user(target_username)

    if target_user is None:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )


    # -----------------------------------------------------
    # PREVENT ADMIN FROM REMOVING THEIR OWN ADMIN ROLE
    # -----------------------------------------------------

    if (
        target_username == username
        and new_role != "admin"
    ):

        raise HTTPException(

            status_code=400,

            detail=(
                "You cannot remove your own "
                "administrator role."
            )

        )


    updated = update_user_role(

        target_username,

        new_role

    )


    if not updated:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )


    return {

        "message":
            "User role updated successfully",

        "username":
            target_username,

        "role":
            new_role

    }


# =========================================================
# ADMIN - DELETE USER
# =========================================================

@app.delete("/admin/users/{target_username}")
def admin_delete_user(

    target_username: str,

    username: str = Depends(
        require_admin
    )

):

    # -----------------------------------------------------
    # PREVENT SELF DELETE
    # -----------------------------------------------------

    if target_username == username:

        raise HTTPException(

            status_code=400,

            detail=(
                "You cannot delete your own "
                "administrator account."
            )

        )


    # -----------------------------------------------------
    # CHECK USER
    # -----------------------------------------------------

    target_user = get_user(target_username)

    if target_user is None:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )


    deleted = delete_user(
        target_username
    )


    if not deleted:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )


    return {

        "message":
            "User deleted successfully",

        "username":
            target_username

    }


# =========================================================
# ADMIN - USER DETAILS
# =========================================================

@app.get("/admin/users/{target_username}")
def admin_get_user(

    target_username: str,

    username: str = Depends(
        require_admin
    )

):

    target_user = get_user(target_username)

    if target_user is None:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )


    user = get_user(target_username)


    return {

        "username":
            target_username,

        "role":
            user["role"]

    }


# =========================================================
# CURRENT USER INFORMATION
# =========================================================

@app.get("/auth/me")
def get_current_user_info(

    username: str = Depends(
        get_current_username
    )

):

    user = get_user(username)


    if user is None:

        raise HTTPException(

            status_code=401,

            detail="User not found"

        )


    return {

        "username":
            username,

        "role":
            user["role"]

    }


# =========================================================
# STARTUP INFORMATION
# =========================================================

@app.on_event("startup")
def startup_message():

    print("")
    print("=" * 60)
    print("AI AGENT SECURITY TESTING PLATFORM")
    print("=" * 60)
    print("")
    print("Application started successfully.")
    print("")
    print("Available agents:")
    print("  secure")
    print("  vulnerable")
    print("")
    print("Chat endpoint:")
    print("  POST /agent/chat")
    print("")
    print("Security scan:")
    print("  POST /security/scan/secure")
    print("  POST /security/scan/vulnerable")
    print("")
    print("Authentication:")
    print("  POST /auth/login")
    print("  GET  /auth/me")
    print("")
    print("Admin:")
    print("  GET    /admin")
    print("  GET    /admin/users")
    print("  POST   /admin/users")
    print("  PUT    /admin/users/{username}/role")
    print("  DELETE /admin/users/{username}")
    print("")
    print("=" * 60)
    print("")
