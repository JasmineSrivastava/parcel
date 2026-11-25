# Parcel Service - CLI Application (v5)

A console-based parcel booking app built with Python and SQLite3. It has two roles: Customer and Officer.

## Requirements
- Python 3.8+
- No extra packages (uses the built-in `sqlite3`)

## How to run
```
python main.py
```
`parcel.db` is created automatically on first run. If you have an older `parcel.db`, delete it first because the table definitions changed.

## Project structure
```
main.py                      Entry point: connect DB, registration / login, hand over to the role menu
database/
    db_setup.py              get_connection() and init_db() (creates tables, loads default users)
menus/
    customer_menu.py         Customer menu loop, home, contact support, booking for self
    officer_menu.py          Officer menu loop, home, booking for a chosen customer
models/
    user.py                  User
    booking.py               Booking
    tracking_info.py         TrackingInfo
    booking_history.py       BookingHistory
services/
    auth_service.py          Registration, login, authentication, authorization
    booking_service.py       Booking, pickup/drop update, delivery status update
    tracking_service.py      Tracking, booking history, invoice
utils/
    validators.py            All input validation functions
    helpers.py               ask, choose, print_table
```

## Database
Created in Python with `sqlite3` (no .sql files). All SQL is written as plain strings inside `cur.execute(...)`.

- `tbl_UserProfile`: User_ID (auto-increment, primary key), UserName (unique), FullName, Address, Email (unique), CountryCode, MobileNumber (unique), Password, Role, Preferences
- `tbl_Booking`: Booking_ID (auto-increment, primary key), User_ID (links to tbl_UserProfile), receiver and parcel details, service cost, payment time, status

One user can have many bookings. Each booking belongs to exactly one user.

### User ID scheme
- IDs 1 to 100 are reserved for officers and are entered by hand in `init_db()`.
- IDs from 101 are for customers. The first default customer is 101, and every customer who registers gets the next number automatically (102, 103, ...).
- The table enforces this: an Officer must have an ID between 1 and 100, and a Customer must have an ID above 100.

## Default logins
| Role     | User ID | User Name | Password   |
|----------|---------|-----------|------------|
| Officer  | 1       | kavita_o  | Kavita@123 |
| Officer  | 2       | sameer_o  | Sameer@123 |
| Customer | 101     | aarav_s   | Aarav@123  |

Login uses User Name and password. After login, the User ID is kept for the session and all data is fetched with it.
To add another officer, add a row with an ID from 1 to 100 in `init_db()` in `database/db_setup.py`. Only customers can register.

## Flow
`main.py` shows Register / Log in / Exit. After login it opens the customer menu or the officer menu depending on the role. Each menu file has its own option list and decides how its role starts a feature, for example a customer books for themselves while an officer first picks the customer.

## Services and the model classes they use

### menus/customer_menu.py and menus/officer_menu.py
| Function | What it does | Model |
|----------|--------------|-------|
| `run` | Shows the role's menu and calls the right service. Re-checks authorization each time. | logged-in `User` |
| `home` | Welcome screen. | `User` |
| `contact_support` (customer) | Shows support contact details. | `User` |
| `book_for_self` (customer) | Starts a booking where the sender is the customer. | `User` |
| `select_customer` (officer) | Asks for a Customer ID and checks it belongs to a customer. | returns `User` |
| `book_for_customer` (officer) | Starts a booking for the chosen customer. | `User` |

### services/auth_service.py
| Function | What it does | Model |
|----------|--------------|-------|
| `register_user` | Registers a customer. Validates every field, makes sure email, mobile and User Name are not already used, and shows the new User ID. | none (values go straight into the table) |
| `login_user` | Checks User Name and password (3 attempts), finds the User ID and loads the user. | returns `User` |
| `get_user_by_id` | Loads a user by User ID. | returns `User` |
| `user_name_taken` | Checks whether a User Name already exists. | none (True or False) |
| `authenticate` | Confirms the user still exists and the role matches the database. | reads `User` |
| `authorize` | Runs `authenticate`, then checks the role is allowed for the feature. | reads `User` |

### services/booking_service.py
| Function | What it does | Model |
|----------|--------------|-------|
| `book_service` | Takes the sender chosen by the menu, captures receiver and parcel details, calculates cost, confirms, saves, prints the invoice. A customer can only book for themselves. | creates `Booking`; reads `User` |
| `calculate_cost` | Works out the service cost from weight, delivery type and packing. | none (returns a number) |
| `save_booking` | Inserts a booking into `tbl_Booking`. | reads `Booking` |
| `get_booking_details` | Asks for a Booking ID and loads its tracking details. | returns `TrackingInfo` |
| `update_pickup_drop` | Officer only. Updates pickup and dropoff times. | `TrackingInfo` |
| `update_delivery_status` | Officer only. Updates status to Booked, In Transit, Delivered or Returned. | `TrackingInfo` |

### services/tracking_service.py
| Function | What it does | Model |
|----------|--------------|-------|
| `track_parcel` | Asks for a Booking ID and shows its status. A customer can only see their own booking. An officer can see any. | `TrackingInfo` |
| `find_tracking` | Fetches one booking's tracking details. | returns `TrackingInfo` |
| `booking_history` | Customer: latest 10 bookings. Officer: all bookings in a date range. | `BookingHistory` |
| `get_history` | Runs the history query. | returns list of `BookingHistory` |
| `generate_invoice` | Asks for a Booking ID and prints the invoice. | `Booking` |
| `fetch_invoice` | Fetches the booking for the invoice. | returns `Booking` |
| `print_invoice` | Prints the invoice details. | reads `Booking` |

## Model classes
Each class has a `from_row(row)` method that fills the object from a database row.

| Class | File | Holds | Extra methods |
|-------|------|-------|---------------|
| `User` | models/user.py | User ID, user name, full name, address, email, country code, mobile, password, role, preferences | |
| `Booking` | models/booking.py | Booking ID, user ID, receiver and parcel details, cost, payment time, status | |
| `TrackingInfo` | models/tracking_info.py | Booking ID, sender name and address, receiver name and address, booking date, status, pickup and dropoff time | `tracking_row()`, `schedule_row()` |
| `BookingHistory` | models/booking_history.py | Customer ID, booking ID, booking date, receiver name, delivered address, amount, status | `row()` |

Results with only one or two values (like a True/False or a cost) are plain values, not objects.

## Menus
**Customer:** Home, Booking Service, Tracking, Previous Booking, Generate Invoice, Contact Support, Logout

**Officer:** Home, Booking Service, Tracking, Delivery Status, Pickup Scheduling, Previous Booking, Generate Invoice, Logout

## Tracking and history
- Tracking: enter a Booking ID. The app checks the booking exists (and, for a customer, that it belongs to them) and shows its status.
- Previous Booking (customer): the customer's latest 10 bookings, newest first.
- Previous Booking (officer): bookings of all customers within a date range, newest first. The Customer ID column shows whose booking each one is.

## Access control
Every feature calls `authorize` first. It checks authentication (the user still exists with the same role) and authorization (the role is allowed for that feature). Customers only see their own bookings and invoices. Officers can view any booking.

## Rules and validation
- Registration is for customers only. Officers cannot self-register.
- Email, mobile number and User Name must each be unique. If one is already used, the app says so and asks for another.
- Name: max 50 characters, letters only
- Email: valid format
- Mobile: exactly 10 digits, country code chosen from a list
- Address: must include a ZIP/PIN code
- User Name: 5-20 characters, letters, digits and underscore
- Password: 6-30 characters with an upper case letter, a lower case letter and a special character
- Pickup time: from the current date and time up to 50 days ahead
- Dropoff time: at least 24 hours after the pickup time

## Service cost
(50 + 20 per 500g of weight) x delivery multiplier (Standard 1.0, Express 1.5, Overnight 2.0) + packing charge (Basic 0, Standard 30, Premium 60)
#   p a r c e l  
 