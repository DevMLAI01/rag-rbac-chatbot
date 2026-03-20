import hashlib
from src.auth.models import UserRecord


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# In-memory demo user registry
_USERS: dict[str, UserRecord] = {
    u.username: u
    for u in [
        UserRecord(user_id="u001", username="finance_user",   hashed_password=_hash("Password123"), role="finance",     display_name="Alex Chen"),
        UserRecord(user_id="u002", username="marketing_user", hashed_password=_hash("Password123"), role="marketing",   display_name="Jordan Kim"),
        UserRecord(user_id="u003", username="hr_user",        hashed_password=_hash("Password123"), role="hr",          display_name="Taylor Patel"),
        UserRecord(user_id="u004", username="eng_user",       hashed_password=_hash("Password123"), role="engineering", display_name="Morgan Rodriguez"),
        UserRecord(user_id="u005", username="ceo",            hashed_password=_hash("Password123"), role="clevel",      display_name="Casey Williams"),
        UserRecord(user_id="u006", username="employee1",      hashed_password=_hash("Password123"), role="employee",    display_name="Riley Thompson"),
    ]
}


def authenticate(username: str, password: str) -> UserRecord | None:
    user = _USERS.get(username)
    if user and user.hashed_password == _hash(password):
        return user
    return None


def get_by_id(user_id: str) -> UserRecord | None:
    return next((u for u in _USERS.values() if u.user_id == user_id), None)
