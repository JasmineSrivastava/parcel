import math
from datetime import datetime

from utils import helpers as h, validators as v
from models.booking import Booking
from services import auth_service, tracking_service

DELIVERY_TYPES = {"Standard": 1.0, "Express": 1.5, "Overnight": 2.0}
PACKING_OPTIONS = {"Basic": 0, "Standard": 30, "Premium": 60}


def calculate_cost(weight_gram, delivery_type, packing):
    weight_charge = math.ceil(weight_gram / 500) * 20
    return round((50 + weight_charge) * DELIVERY_TYPES[delivery_type] + PACKING_OPTIONS[packing], 2)


def save_booking(cur, b):
    cur.execute(
        """INSERT INTO tbl_Booking
           (User_ID, Rec_Name, Rec_Address, Rec_Pin, Rec_Mobile, Par_Weight_Gram,
            Par_Contents_Description, Par_Delivery_Type, Par_Packing_Preference,
            Par_PickupTime, Par_DropoffTime, Par_ServiceCost, Par_PaymentTime, Par_Status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [b.user_id, b.rec_name, b.rec_address, b.rec_pin, b.rec_mobile, b.weight_gram, b.contents,
         b.delivery_type, b.packing, b.pickup_time, b.dropoff_time, b.service_cost, b.payment_time, b.status])
    cur.connection.commit()
    return cur.lastrowid


def book_service(cur, user, sender):
    if not auth_service.authorize(cur, user, ["Customer", "Officer"]):
        return

    if sender.role != "Customer":
        print("  [Error] Bookings can only be made for customers.")
        return
    if user.role == "Customer" and sender.user_id != user.user_id:
        print("  [Error] Access denied. Customers can only book for themselves.")
        return

    print("\n--- Sender Details ---")
    print(f"Name    : {sender.full_name}")
    print(f"Address : {sender.address}")
    print(f"Contact : {sender.country_code} {sender.mobile}")

    print("\n--- Receiver & Parcel Details ---")
    rec_name = h.ask("Receiver Name (max 50 chars)", lambda x: v.validate_name(x, "Receiver name"))
    rec_address = h.ask("Receiver Address", lambda x: v.validate_text(x, "Receiver address", 200))
    rec_pin = h.ask("Receiver PIN (6 digits)", v.validate_pin)
    rec_mobile = h.ask("Receiver Mobile (10 digits)", v.validate_mobile)
    weight = int(h.ask("Parcel Weight in grams", v.validate_weight))
    contents = h.ask("Parcel Contents Description", lambda x: v.validate_text(x, "Contents description"))
    delivery = h.choose("Delivery Type", list(DELIVERY_TYPES))
    packing = h.choose("Packing Preference", list(PACKING_OPTIONS))
    pickup = h.ask("Pickup Time (YYYY-MM-DD HH:MM)", v.validate_pickup_time)
    dropoff = h.ask("Dropoff Time (YYYY-MM-DD HH:MM)", v.make_drop_validator(pickup))

    cost = calculate_cost(weight, delivery, packing)
    print(f"\nCalculated Service Cost: {cost:.2f}")
    if h.choose("Confirm booking?", ["Yes", "No"]) == "No":
        print("Booking cancelled.")
        return

    booking = Booking(sender.user_id, rec_name, rec_address, rec_pin, rec_mobile, weight, contents,
                      delivery, packing, pickup, dropoff, cost,
                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    booking.booking_id = save_booking(cur, booking)
    print(f"\nBooking successful! Your Booking ID is {booking.booking_id}.")
    tracking_service.print_invoice(booking)


def get_booking_details(cur):
    booking_id = int(h.ask("Enter Booking ID", lambda x: v.validate_positive_int(x, "Booking ID")))
    info = tracking_service.find_tracking(cur, booking_id)
    if info is None:
        print("  [Error] No booking found with that Booking ID.")
    return info


def update_pickup_drop(cur, user):
    print("\n===== PICKUP SCHEDULING =====")
    if not auth_service.authorize(cur, user, ["Officer"]):
        return

    info = get_booking_details(cur)
    if info is None:
        return
    schedule_headers = tracking_service.TRACK_HEADERS + ["Par_PickupTime", "Par_DropoffTime"]
    h.print_table(schedule_headers, [info.schedule_row()])

    pickup = h.ask("New Pickup Time (YYYY-MM-DD HH:MM)", v.validate_pickup_time)
    dropoff = h.ask("New Dropoff Time (YYYY-MM-DD HH:MM)", v.make_drop_validator(pickup))

    cur.execute("UPDATE tbl_Booking SET Par_PickupTime = ?, Par_DropoffTime = ? WHERE Booking_ID = ?",
                (pickup, dropoff, info.booking_id))
    cur.connection.commit()
    print("Pickup and dropoff times updated successfully.")


def update_delivery_status(cur, user):
    print("\n===== DELIVERY STATUS UPDATE =====")
    if not auth_service.authorize(cur, user, ["Officer"]):
        return

    info = get_booking_details(cur)
    if info is None:
        return
    h.print_table(tracking_service.TRACK_HEADERS, [info.tracking_row()])

    statuses = ["Booked", "In Transit", "Delivered", "Returned"]
    status = h.choose("Select new status", statuses)
    if status == info.status:
        print(f"  Status is already '{status}'. No change made.")
        return
    cur.execute("UPDATE tbl_Booking SET Par_Status = ? WHERE Booking_ID = ?", (status, info.booking_id))
    cur.connection.commit()
    print(f"Delivery status updated to '{status}'.")
