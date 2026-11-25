from datetime import date

from utils import helpers as h, validators as v
from services import auth_service
from models.booking import Booking
from models.booking_history import BookingHistory
from models.tracking_info import TrackingInfo

TRACK_HEADERS = ["Booking ID", "FullName", "Address", "Rec_Name", "Rec_Address", "Date of Booking", "Par_Status"]


def find_tracking(cur, booking_id, user_id=None):
    if user_id is None:
        cur.execute("""SELECT b.Booking_ID, u.FullName, u.Address, b.Rec_Name, b.Rec_Address,
                              b.Par_PaymentTime, b.Par_Status, b.Par_PickupTime, b.Par_DropoffTime
                       FROM tbl_Booking b JOIN tbl_UserProfile u ON u.User_ID = b.User_ID
                       WHERE b.Booking_ID = ?""", (booking_id,))
    else:
        cur.execute("""SELECT b.Booking_ID, u.FullName, u.Address, b.Rec_Name, b.Rec_Address,
                              b.Par_PaymentTime, b.Par_Status, b.Par_PickupTime, b.Par_DropoffTime
                       FROM tbl_Booking b JOIN tbl_UserProfile u ON u.User_ID = b.User_ID
                       WHERE b.Booking_ID = ? AND b.User_ID = ?""", (booking_id, user_id))
    row = cur.fetchone()
    return TrackingInfo().from_row(row) if row else None


def track_parcel(cur, user):
    print("\n===== TRACKING STATUS =====")
    if not auth_service.authorize(cur, user, ["Customer", "Officer"]):
        return
    booking_id = int(h.ask("Enter Booking ID", lambda x: v.validate_positive_int(x, "Booking ID")))
    if user.role == "Officer":
        info = find_tracking(cur, booking_id)
    else:
        info = find_tracking(cur, booking_id, user.user_id)
    if info is None:
        print("  [Error] No booking found with that Booking ID.")
    else:
        h.print_table(TRACK_HEADERS, [info.tracking_row()])


def get_history(cur, user_id, start=None, end=None):
    if start is None:
        cur.execute("""SELECT User_ID, Booking_ID, Par_PaymentTime, Rec_Name, Rec_Address,
                              Par_ServiceCost, Par_Status
                       FROM tbl_Booking
                       WHERE User_ID = ?
                       ORDER BY Par_PaymentTime DESC, Booking_ID DESC
                       LIMIT 10""", (user_id,))
    else:
        cur.execute("""SELECT User_ID, Booking_ID, Par_PaymentTime, Rec_Name, Rec_Address,
                              Par_ServiceCost, Par_Status
                       FROM tbl_Booking
                       WHERE User_ID = ?
                         AND date(Par_PaymentTime) BETWEEN ? AND ?
                       ORDER BY Par_PaymentTime DESC, Booking_ID DESC""", (user_id, start, end))
    return [BookingHistory().from_row(r) for r in cur.fetchall()]


def booking_history(cur, user):
    print("\n===== PREVIOUS BOOKINGS =====")
    if not auth_service.authorize(cur, user, ["Customer", "Officer"]):
        return
    if user.role == "Officer":
        while True:
            customer_id = int(h.ask("Enter Customer ID", lambda x: v.validate_positive_int(x, "Customer ID")))
            customer = auth_service.get_user_by_id(cur, customer_id)
            if customer is not None and customer.role == "Customer":
                break
            print("  [Error] No customer found with that Customer ID.")

        start = h.ask("From date (YYYY-MM-DD)", v.validate_date)

        def end_check(x):
            err = v.validate_date(x)
            if err:
                return err
            if x < start:
                return "End date cannot be before start date."
            if x > date.today().isoformat():
                return "End date cannot be after today."
            return None

        end = h.ask("To date (YYYY-MM-DD)", end_check)
        records = get_history(cur, customer_id, start, end)
    else:
        records = get_history(cur, user.user_id)
    history_headers = ["Customer ID", "Booking ID", "Booking Date", "Receiver Name",
                       "Delivered address", "Amount", "Status"]
    h.print_table(history_headers, [h.row() for h in records])


def fetch_invoice(cur, booking_id, user):
    if user.role == "Officer":
        cur.execute("SELECT * FROM tbl_Booking WHERE Booking_ID = ?", (booking_id,))
    else:
        cur.execute("SELECT * FROM tbl_Booking WHERE Booking_ID = ? AND User_ID = ?", (booking_id, user.user_id))
    row = cur.fetchone()
    return Booking().from_row(row) if row else None


def print_invoice(b):
    print("\n========== INVOICE ==========")
    print(f"Booking ID              : {b.booking_id}")
    print(f"Receiver Name           : {b.rec_name}")
    print(f"Receiver Address        : {b.rec_address}")
    print(f"Receiver Pin            : {b.rec_pin}")
    print(f"Receiver Mobile         : {b.rec_mobile}")
    print(f"Parcel Weight(g)        : {b.weight_gram}")
    print(f"Contents Description    : {b.contents}")
    print(f"Delivery Type           : {b.delivery_type}")
    print(f"Packing Preference      : {b.packing}")
    print(f"Pickup Time             : {b.pickup_time}")
    print(f"Dropoff Time            : {b.dropoff_time}")
    print(f"Service Cost            : {b.service_cost:.2f}")
    print(f"Payment Time            : {b.payment_time}")
    print("=============================")


def generate_invoice(cur, user):
    print("\n===== GENERATE INVOICE =====")
    if not auth_service.authorize(cur, user, ["Customer", "Officer"]):
        return
    booking_id = h.ask("Enter Booking ID", lambda x: v.validate_positive_int(x, "Booking ID"))
    booking = fetch_invoice(cur, int(booking_id), user)
    if booking is None:
        print("  [Error] No booking found with that Booking ID for your account.")
    else:
        print_invoice(booking)
