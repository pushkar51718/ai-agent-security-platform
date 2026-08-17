from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from fastapi import HTTPException, Header
from pwdlib import PasswordHash


# =========================================================
# JWT CONFIGURATION
# =========================================================

SECRET_KEY = "ai-agent-security-platform-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =========================================================
# PASSWORD HASHING
# =========================================================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a password securely.
    """
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a password against its stored hash.
    """
    try:
        return password_hash.verify(
            plain_password,
            hashed_password
        )
    except Exception:
        return False


# =========================================================
# CREATE JWT TOKEN
# =========================================================

def create_access_token(username: str) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_username(
    authorization: str | None = Header(default=None)
) -> str:

    # -----------------------------------------------------
    # Authorization header missing
    # -----------------------------------------------------

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # -----------------------------------------------------
    # Check Bearer format
    # -----------------------------------------------------

    parts = authorization.split(" ", 1)

    if len(parts) != 2:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    scheme, token = parts

    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication scheme"
        )

    # -----------------------------------------------------
    # Decode JWT
    # -----------------------------------------------------

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token"
        )