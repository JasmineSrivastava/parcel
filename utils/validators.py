import re
from datetime import datetime, timedelta

COUNTRY_CODES = ["+91", "+1", "+44", "+61", "+971"]
DATE_FMT = "%Y-%m-%d %H:%M"


def validate_name(v, label="Name"):
    v = v.strip()
    if not v:
        return f"{label} cannot be empty."
    if len(v) > 50:
        return f"{label} must be at most 50 characters (you entered {len(v)})."
    if not re.fullmatch(r"[A-Za-z][A-Za-z ]*", v):
        return f"{label} can only contain letters, spaces, . ' and -."
    return None


def validate_email(v):
    if not v.strip():
        return "Email cannot be empty."
    if not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", v.strip()):
        return "Invalid email format (example: name@example.com)."
    return None


def validate_mobile(v):
    if not v.isdigit():
        return "Mobile number must contain digits only."
    if len(v) != 10:
        return f"Mobile number must be exactly 10 digits (you entered {len(v)})."
    return None


def validate_address(v):
    v = v.strip()
    if not v:
        return "Address cannot be empty."
    if len(v) > 200:
        return "Address must be at most 200 characters."
    if not re.search(r"\b\d{5,6}\b", v):
        return "Address must include the ZIP/PIN code (5-6 digits)."
    return None


def validate_user_name(v):
    if not (5 <= len(v) <= 20):
        return f"User Name must be 5 to 20 characters (you entered {len(v)})."
    if not re.fullmatch(r"\w+", v):
        return "User Name can contain only letters, digits and underscore."
    return None


def validate_password(v):
    if len(v) > 30:
        return "Password must be at most 30 characters."
    if len(v) < 6:
        return "Password must be at least 6 characters."
    if not re.search(r"[A-Z]", v):
        return "Password needs at least one upper case letter."
    if not re.search(r"[a-z]", v):
        return "Password needs at least one lower case letter."
    if not re.search(r"[^A-Za-z0-9]", v):
        return "Password needs at least one special character."
    return None


def validate_pin(v):
    if not (v.isdigit() and len(v) == 6):
        return "PIN must be exactly 6 digits."
    return None


def validate_weight(v):
    if not v.isdigit() or int(v) <= 0:
        return "Weight must be a positive whole number (grams)."
    if int(v) > 30000:
        return "Maximum allowed weight is 30000 grams."
    return None


def validate_text(v, label, max_len=100):
    if not v.strip():
        return f"{label} cannot be empty."
    if len(v.strip()) > max_len:
        return f"{label} must be at most {max_len} characters."
    return None


def validate_datetime(v):
    try:
        datetime.strptime(v, DATE_FMT)
    except ValueError:
        return "Invalid format. Use YYYY-MM-DD HH:MM (example: 2026-12-01 14:30)."
    return None


def validate_date(v):
    try:
        datetime.strptime(v, "%Y-%m-%d")
    except ValueError:
        return "Invalid date. Use YYYY-MM-DD (example: 2026-12-01)."
    return None


def validate_positive_int(v, label="ID"):
    if not v.isdigit() or int(v) <= 0:
        return f"{label} must be a positive number."
    return None


def validate_pickup_time(x):
    err = validate_datetime(x)
    if err:
        return err
    pickup = datetime.strptime(x, DATE_FMT)
    now = datetime.now().replace(second=0, microsecond=0)
    latest = now + timedelta(days=50)
    if pickup < now:
        return "Pickup time cannot be in the past."
    if pickup > latest:
        return f"Pickup time must be within the next 50 days (latest: {latest.strftime(DATE_FMT)})."
    return None


def make_drop_validator(pickup):
    def check(x):
        err = validate_datetime(x)
        if err:
            return err
        earliest = datetime.strptime(pickup, DATE_FMT) + timedelta(hours=24)
        if datetime.strptime(x, DATE_FMT) < earliest:
            return f"Dropoff time must be at least 24 hours after pickup (earliest: {earliest.strftime(DATE_FMT)})."
        return None
    return check
