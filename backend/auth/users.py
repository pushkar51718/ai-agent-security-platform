# =========================================================
# PERSISTENT USER DATABASE
# SQLite + Password Hashing + Role Management
# =========================================================

import sqlite3
from pathlib import Path

from backend.auth.auth import hash_password


# =========================================================
# DATABASE LOCATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_FILE = DATABASE_DIR / "users.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    connection = sqlite3.connect(
        str(DATABASE_FILE)
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# CREATE DATABASE TABLE
# =========================================================

def initialize_database():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password_hash TEXT NOT NULL,

                role TEXT NOT NULL DEFAULT 'user'

            )
            """
        )

        connection.commit()

    finally:

        connection.close()


# =========================================================
# CREATE DEFAULT USERS
# =========================================================

def initialize_default_users():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        default_users = [

            (
                "admin",
                "admin123",
                "admin"
            ),

            (
                "security",
                "security123",
                "security_analyst"
            )

        ]

        for username, password, role in default_users:

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                """,
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user is None:

                cursor.execute(
                    """
                    INSERT INTO users
                    (
                        username,
                        password_hash,
                        role
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        username,
                        hash_password(password),
                        role
                    )
                )

        connection.commit()

    finally:

        connection.close()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

initialize_database()

initialize_default_users()


# =========================================================
# GET USER
# =========================================================

def get_user(username):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                username,
                password_hash,
                role
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        row = cursor.fetchone()

        if row is None:

            return None

        return {

            "username":
                row["username"],

            "password_hash":
                row["password_hash"],

            "role":
                row["role"]

        }

    finally:

        connection.close()


# =========================================================
# GET ALL USERS
# =========================================================

def get_all_users():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                username,
                role
            FROM users
            ORDER BY username
            """
        )

        rows = cursor.fetchall()

        return [

            {

                "username":
                    row["username"],

                "role":
                    row["role"]

            }

            for row in rows

        ]

    finally:

        connection.close()


# =========================================================
# CREATE USER
# =========================================================

def create_user(
    username,
    password,
    role
):

    username = str(
        username
    ).strip()

    role = str(
        role
    ).strip().lower()


    if not username:

        return False


    if not password:

        return False


    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password_hash,
                role
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                hash_password(password),
                role
            )
        )

        connection.commit()

        return True


    except sqlite3.IntegrityError:

        return False


    finally:

        connection.close()


# =========================================================
# DELETE USER
# =========================================================

def delete_user(username):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE username = ?
            """,
            (username,)
        )

        deleted = cursor.rowcount > 0

        connection.commit()

        return deleted

    finally:

        connection.close()


# =========================================================
# UPDATE USER ROLE
# =========================================================

def update_user_role(
    username,
    role
):

    role = str(
        role
    ).strip().lower()


    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET role = ?
            WHERE username = ?
            """,
            (
                role,
                username
            )
        )

        updated = cursor.rowcount > 0

        connection.commit()

        return updated

    finally:

        connection.close()