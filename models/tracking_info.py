class TrackingInfo:
    def __init__(self, booking_id=None, full_name=None, address=None, rec_name=None, rec_address=None,
                 booking_date=None, status=None, pickup_time=None, dropoff_time=None):
        self.booking_id = booking_id
        self.full_name = full_name
        self.address = address
        self.rec_name = rec_name
        self.rec_address = rec_address
        self.booking_date = booking_date
        self.status = status
        self.pickup_time = pickup_time
        self.dropoff_time = dropoff_time

    def from_row(self, r):
        self.booking_id = r["Booking_ID"]
        self.full_name = r["FullName"]
        self.address = r["Address"]
        self.rec_name = r["Rec_Name"]
        self.rec_address = r["Rec_Address"]
        self.booking_date = r["Par_PaymentTime"]
        self.status = r["Par_Status"]
        self.pickup_time = r["Par_PickupTime"]
        self.dropoff_time = r["Par_DropoffTime"]
        return self

    def tracking_row(self):
        return [self.booking_id, self.full_name, self.address, self.rec_name,
                self.rec_address, self.booking_date, self.status]

    def schedule_row(self):
        return self.tracking_row() + [self.pickup_time, self.dropoff_time]
