from services import auth_service, booking_service, tracking_service
from utils import helpers as h


def home(cur, user):
    print("\n===== HOME =====")
    if not auth_service.authorize(cur, user, ["Customer"]):
        return
    print(f"Welcome, {user.full_name}!  (User ID: {user.user_id})")
    print("You can book a service, track parcels, view previous bookings and invoices.")


def contact_support(cur, user):
    print("\n===== CONTACT SUPPORT =====")
    if not auth_service.authorize(cur, user, ["Customer"]):
        return
    print("Email : support@parcelservice.com")
    print("Phone : +91 1800-123-456  (Mon-Sat, 9am - 6pm)")


def book_for_self(cur, user):
    print("\n===== BOOKING SERVICE =====")
    booking_service.book_service(cur, user, user)


def run(cur, user):
    options = ["Home", "Booking Service", "Tracking", "Previous Booking",
               "Generate Invoice", "Contact Support", "Logout"]
    while True:
        if not auth_service.authorize(cur, user, ["Customer"]):
            return
        choice = h.choose("===== CUSTOMER MENU =====", options)
        if choice == "Home":
            home(cur, user)
        elif choice == "Booking Service":
            book_for_self(cur, user)
        elif choice == "Tracking":
            tracking_service.track_parcel(cur, user)
        elif choice == "Previous Booking":
            tracking_service.booking_history(cur, user)
        elif choice == "Generate Invoice":
            tracking_service.generate_invoice(cur, user)
        elif choice == "Contact Support":
            contact_support(cur, user)
        elif choice == "Logout":
            print("You have been logged out.")
            return
