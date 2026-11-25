from utils import helpers as h, validators as v
from models.user import User


def get_user_by_id(cur, user_id):
    cur.execute("SELECT * FROM tbl_UserProfile WHERE User_ID = ?", (user_id,))
    row = cur.fetchone()
    return User().from_row(row) if row else None


def user_name_taken(cur, user_name):
    cur.execute("SELECT 1 FROM tbl_UserProfile WHERE UserName = ?", (user_name,))
    return cur.fetchone() is not None


def register_user(cur):
    print("\n===== USER REGISTRATION =====")
    role = "Customer"

    name = h.ask("Full Name (max 50 chars)", lambda x: v.validate_name(x, role + " name"))

    def email_check(x):
        err = v.validate_email(x)
        if err:
            return err
        cur.execute("SELECT 1 FROM tbl_UserProfile WHERE lower(Email) = lower(?)", (x,))
        return "This email is already registered. Please enter another email." if cur.fetchone() else None
    email = h.ask("Email", email_check)

    code = h.choose("Choose country code", v.COUNTRY_CODES)
    def mobile_check(x):
        err = v.validate_mobile(x)
        if err:
            return err
        cur.execute("SELECT 1 FROM tbl_UserProfile WHERE MobileNumber = ?", (x,))
        return "This mobile number is already registered. Please enter another mobile number." if cur.fetchone() else None
    mobile = h.ask("Mobile number (10 digits)", mobile_check)
    address = h.ask("Complete mailing address (include ZIP/PIN code)", v.validate_address)

    def user_check(x):
        err = v.validate_user_name(x)
        if err:
            return err
        return "This User Name is already taken. Please enter another User Name." if user_name_taken(cur, x) else None
    user_name = h.ask("User Name for login (5-20 chars)", user_check)

    while True:
        password = h.ask("Password (max 30; upper, lower & special char)", v.validate_password)
        confirm = input("Confirm Password: ").strip()
        if password == confirm:
            break
        print("  [Error] Passwords do not match. Please try again.")

    preferences = ["Email", "SMS", "Email and SMS", "None"]
    pref = h.choose("Notification / mail delivery preference", preferences)

    values = [user_name, name, address, email, code, mobile, password, role, pref]
    cur.execute(
        """INSERT INTO tbl_UserProfile
           (UserName, FullName, Address, Email, CountryCode, MobileNumber, Password, Role, Preferences)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", values)
    cur.connection.commit()
    new_id = cur.lastrowid
    print(f"\nRegistration successful! Your User ID is {new_id}.")
    print(f"You can now log in as {role} with User Name '{user_name}'.")


def login_user(cur):
    print("\n===== LOGIN =====")
    for attempt in range(1, 4):
        user_name = h.ask("User Name", v.validate_user_name)
        password = h.ask("Password", v.validate_password)

        cur.execute("SELECT User_ID, Password FROM tbl_UserProfile WHERE UserName = ?", (user_name,))
        credentials = cur.fetchone()
        if credentials is None:
            print("  [Error] User Name not found.")
        elif credentials["Password"] != password:
            print("  [Error] Incorrect password.")
        else:
            user = get_user_by_id(cur, credentials["User_ID"])
            print(f"\nLogin successful. Welcome, {user.full_name} ({user.role})!")
            return user
        print(f"  Attempt {attempt} of 3 failed.")
    print("Too many failed attempts. Returning to main menu.")
    return None


def authenticate(cur, user):
    if user is None:
        return False
    cur.execute("SELECT Role FROM tbl_UserProfile WHERE User_ID = ?", (user.user_id,))
    row = cur.fetchone()
    return row is not None and row["Role"] == user.role


def authorize(cur, user, allowed_roles):
    if not authenticate(cur, user):
        print("  [Error] Authentication failed. Please log in again.")
        return False
    if user.role not in allowed_roles:
        print(f"  [Error] Access denied. This option is not available for the {user.role} role.")
        return False
    return True
