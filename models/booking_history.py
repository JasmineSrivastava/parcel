class BookingHistory:
    def __init__(self, customer_id=None, booking_id=None, booking_date=None, receiver_name=None,
                 delivered_address=None, amount=None, status=None):
        self.customer_id = customer_id
        self.booking_id = booking_id
        self.booking_date = booking_date
        self.receiver_name = receiver_name
        self.delivered_address = delivered_address
        self.amount = amount
        self.status = status

    def from_row(self, r):
        self.customer_id = r["User_ID"]
        self.booking_id = r["Booking_ID"]
        self.booking_date = r["Par_PaymentTime"]
        self.receiver_name = r["Rec_Name"]
        self.delivered_address = r["Rec_Address"]
        self.amount = r["Par_ServiceCost"]
        self.status = r["Par_Status"]
        return self

    def row(self):
        return [self.customer_id, self.booking_id, self.booking_date, self.receiver_name,
                self.delivered_address, self.amount, self.status]
