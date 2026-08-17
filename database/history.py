# =========================================================
# SCAN HISTORY DATABASE
# =========================================================

from pathlib import Path
import json
from datetime import datetime


# =========================================================
# DATABASE LOCATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

HISTORY_DIR = BASE_DIR / "database"

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True
)

HISTORY_FILE = HISTORY_DIR / "scan_history.json"


# =========================================================
# INITIALIZE HISTORY FILE
# =========================================================

def initialize_history():

    if not HISTORY_FILE.exists():

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


# =========================================================
# READ ALL HISTORY
# =========================================================

def read_all_history():

    initialize_history()

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):

            return []

        return data

    except Exception as error:

        print(
            "HISTORY READ ERROR:",
            repr(error)
        )

        return []


# =========================================================
# WRITE ALL HISTORY
# =========================================================

def write_all_history(history):

    initialize_history()

    temporary_file = HISTORY_FILE.with_suffix(
        ".tmp"
    )

    with open(
        temporary_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )

    temporary_file.replace(
        HISTORY_FILE
    )


# =========================================================
# GET NEXT ID
# =========================================================

def get_next_scan_id(history):

    if not history:

        return 1

    ids = []

    for scan in history:

        try:

            ids.append(
                int(
                    scan.get(
                        "id",
                        0
                    )
                )
            )

        except Exception:

            continue

    if not ids:

        return 1

    return max(ids) + 1


# =========================================================
# SAVE SCAN
# =========================================================

def save_scan(
    username,
    agent,
    security_score,
    risk_level,
    total_tests,
    passed,
    failed,
    results=None
):

    history = read_all_history()

    scan = {

        "id":
            get_next_scan_id(
                history
            ),

        "created_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "username":
            username,

        "agent":
            agent,

        "security_score":
            security_score,

        "risk_level":
            risk_level,

        "total_tests":
            total_tests,

        "passed":
            passed,

        "failed":
            failed,

        "results":
            results
            if isinstance(results, list)
            else []

    }

    history.append(
        scan
    )

    write_all_history(
        history
    )

    return scan


# =========================================================
# FILTER HISTORY
# =========================================================

def filter_history(
    username,
    search="",
    status="",
    risk=""
):

    history = read_all_history()

    username = str(
        username
    ).strip()

    search = str(
        search or ""
    ).strip().lower()

    status = str(
        status or ""
    ).strip().lower()

    risk = str(
        risk or ""
    ).strip().lower()


    # -----------------------------------------------------
    # USER HISTORY
    # -----------------------------------------------------

    history = [

        scan

        for scan in history

        if str(
            scan.get(
                "username",
                ""
            )
        ).strip()
        == username

    ]


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if search:

        filtered = []

        for scan in history:

            searchable_text = " ".join([

                str(
                    scan.get(
                        "agent",
                        ""
                    )
                ),

                str(
                    scan.get(
                        "created_at",
                        ""
                    )
                ),

                str(
                    scan.get(
                        "risk_level",
                        ""
                    )
                ),

                str(
                    scan.get(
                        "security_score",
                        ""
                    )
                )

            ]).lower()


            if search in searchable_text:

                filtered.append(
                    scan
                )

        history = filtered


    # -----------------------------------------------------
    # SECURE / VULNERABLE
    # -----------------------------------------------------

    if status in {
        "secure",
        "vulnerable"
    }:

        filtered = []

        for scan in history:

            agent_name = str(
                scan.get(
                    "agent",
                    ""
                )
            ).lower()


            try:

                score = float(
                    scan.get(
                        "security_score",
                        0
                    )
                )

            except Exception:

                score = 0


            risk_level = str(
                scan.get(
                    "risk_level",
                    ""
                )
            ).lower()


            if status == "secure":

                if (
                    "secure" in agent_name
                    or (
                        score >= 7
                        and
                        risk_level == "low"
                    )
                ):

                    filtered.append(
                        scan
                    )


            elif status == "vulnerable":

                if (
                    "vulnerable" in agent_name
                    or
                    score < 7
                    or
                    risk_level in {
                        "critical",
                        "high",
                        "medium"
                    }
                ):

                    filtered.append(
                        scan
                    )

        history = filtered


    # -----------------------------------------------------
    # RISK FILTER
    # -----------------------------------------------------

    if risk:

        history = [

            scan

            for scan in history

            if str(
                scan.get(
                    "risk_level",
                    ""
                )
            ).lower()
            == risk

        ]


    # -----------------------------------------------------
    # NEWEST FIRST
    # -----------------------------------------------------

    history.sort(

        key=lambda scan:
            scan.get(
                "created_at",
                ""
            ),

        reverse=True

    )

    return history


# =========================================================
# GET USER HISTORY
# =========================================================

def get_history(username):

    return filter_history(
        username=username
    )


# =========================================================
# GET ONE SCAN
# =========================================================

def get_scan(
    username,
    scan_id
):

    history = read_all_history()

    for scan in history:

        if (

            str(
                scan.get(
                    "username",
                    ""
                )
            )
            ==
            str(username)

            and

            str(
                scan.get(
                    "id",
                    ""
                )
            )
            ==
            str(scan_id)

        ):

            return scan

    return None


# =========================================================
# CLEAR USER HISTORY
# =========================================================

def clear_user_history(username):

    history = read_all_history()

    remaining_history = [

        scan

        for scan in history

        if str(
            scan.get(
                "username",
                ""
            )
        )
        != str(username)

    ]

    write_all_history(
        remaining_history
    )

    return True


# =========================================================
# DELETE ONE SCAN
# =========================================================

def delete_scan(
    username,
    scan_id
):

    history = read_all_history()

    new_history = []

    deleted = False

    for scan in history:

        if (

            str(
                scan.get(
                    "username",
                    ""
                )
            )
            ==
            str(username)

            and

            str(
                scan.get(
                    "id",
                    ""
                )
            )
            ==
            str(scan_id)

        ):

            deleted = True

            continue

        new_history.append(
            scan
        )


    if deleted:

        write_all_history(
            new_history
        )


    return deleted