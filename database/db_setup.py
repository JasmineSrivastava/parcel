import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parcel.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    return conn, cur


def init_db(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS tbl_UserProfile (
        User_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
        UserName      TEXT NOT NULL UNIQUE CHECK (length(UserName) BETWEEN 5 AND 20),
        FullName      TEXT NOT NULL CHECK (length(FullName) <= 50),
        Address       TEXT NOT NULL,
        Email         TEXT NOT NULL UNIQUE,
        CountryCode   TEXT NOT NULL,
        MobileNumber  TEXT NOT NULL UNIQUE CHECK (length(MobileNumber) = 10),
        Password      TEXT NOT NULL CHECK (length(Password) <= 30),
        Role          TEXT NOT NULL CHECK (Role IN ('Customer', 'Officer')),
        Preferences   TEXT DEFAULT 'None',
        CHECK ((Role = 'Officer' AND User_ID BETWEEN 1 AND 100)
            OR (Role = 'Customer' AND User_ID > 100)))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tbl_Booking (
        Booking_ID               INTEGER PRIMARY KEY AUTOINCREMENT,
        User_ID                  INTEGER NOT NULL,
        Rec_Name                 TEXT NOT NULL,
        Rec_Address              TEXT NOT NULL,
        Rec_Pin                  TEXT NOT NULL,
        Rec_Mobile               TEXT NOT NULL,
        Par_Weight_Gram          INTEGER NOT NULL,
        Par_Contents_Description TEXT NOT NULL,
        Par_Delivery_Type        TEXT NOT NULL,
        Par_Packing_Preference   TEXT NOT NULL,
        Par_PickupTime           TEXT NOT NULL,
        Par_DropoffTime          TEXT NOT NULL,
        Par_ServiceCost          REAL NOT NULL,
        Par_PaymentTime          TEXT NOT NULL,
        Par_Status               TEXT NOT NULL DEFAULT 'Booked'
            CHECK (Par_Status IN ('Booked', 'In Transit', 'Delivered', 'Returned')),
        FOREIGN KEY (User_ID) REFERENCES tbl_UserProfile (User_ID))""")

    users = [
        (1, "kavita_o", "Kavita Rao", "3 Civil Lines, Delhi 110054", "kavita@example.com", "+91", "9988776655", "Kavita@123", "Officer", "Email"),
        (2, "sameer_o", "Sameer Khan", "22 Anna Salai, Chennai 600002", "sameer@example.com", "+91", "9871234560", "Sameer@123", "Officer", "None"),
        (101, "aarav_s", "Aarav Sharma", "12 MG Road, Bengaluru 560001", "aarav@example.com", "+91", "9876543210", "Aarav@123", "Customer", "Email"),
    ]
    cur.executemany(
        """INSERT OR IGNORE INTO tbl_UserProfile
           (User_ID, UserName, FullName, Address, Email, CountryCode, MobileNumber, Password, Role, Preferences)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", users)
    cur.connection.commit()
