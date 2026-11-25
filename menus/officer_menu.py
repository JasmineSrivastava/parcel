from services import auth_service, booking_service, tracking_service
from utils import helpers as h
from utils import validators as v


def home(cur, user):
    print("\n===== HOME =====")
    if not auth_service.authorize(cur, user, ["Officer"]):
        return
    print(f"Welcome, {user.full_name}!  (User ID: {user.user_id})")
    print("You can track parcels, update delivery status and pickup schedules, book for customers and view invoices.")


def select_customer(cur):
    while True:
        cust_id = int(h.ask("Enter the Customer ID to book for", lambda x: v.validate_positive_int(x, "Customer ID")))
        customer = auth_service.get_user_by_id(cur, cust_id)
        if customer is not None and customer.role == "Customer":
            return customer
        print("  [Error] No customer found with that Customer ID.")


def book_for_customer(cur, user):
    print("\n===== BOOKING SERVICE =====")
    if not auth_service.authorize(cur, user, ["Officer"]):
        return
    customer = select_customer(cur)
    booking_service.book_service(cur, user, customer)


def run(cur, user):
    options = ["Home", "Booking Service", "Tracking", "Delivery Status", "Pickup Scheduling",
               "Previous Booking", "Generate Invoice", "Logout"]
    while True:
        if not auth_service.authorize(cur, user, ["Officer"]):
            return
        choice = h.choose("===== OFFICER MENU =====", options)
        if choice == "Home":
            home(cur, user)
        elif choice == "Booking Service":
            book_for_customer(cur, user)
        elif choice == "Tracking":
            tracking_service.track_parcel(cur, user)
        elif choice == "Delivery Status Update":
            booking_service.update_delivery_status(cur, user)
        elif choice == "Pickup Scheduling":
            booking_service.update_pickup_drop(cur, user)
        elif choice == "Previous Booking":
            tracking_service.booking_history(cur, user)
        elif choice == "Generate Invoice":
            tracking_service.generate_invoice(cur, user)
        elif choice == "Logout":
            print("You have been logged out.")
            return
