class User:
    def __init__(self, user_id=None, user_name=None, full_name=None, address=None, email=None,
                 country_code=None, mobile=None, password=None, role=None, preferences=None):
        self.user_id = user_id
        self.user_name = user_name
        self.full_name = full_name
        self.address = address
        self.email = email
        self.country_code = country_code
        self.mobile = mobile
        self.password = password
        self.role = role
        self.preferences = preferences

    def from_row(self, r):
        self.user_id = r["User_ID"]
        self.user_name = r["UserName"]
        self.full_name = r["FullName"]
        self.address = r["Address"]
        self.email = r["Email"]
        self.country_code = r["CountryCode"]
        self.mobile = r["MobileNumber"]
        self.password = r["Password"]
        self.role = r["Role"]
        self.preferences = r["Preferences"]
        return self
