class Booking:
    def __init__(self, user_id=None, rec_name=None, rec_address=None, rec_pin=None, rec_mobile=None,
                 weight_gram=None, contents=None, delivery_type=None, packing=None,
                 pickup_time=None, dropoff_time=None, service_cost=None, payment_time=None,
                 status="Booked", booking_id=None):
        self.booking_id = booking_id
        self.user_id = user_id
        self.rec_name = rec_name
        self.rec_address = rec_address
        self.rec_pin = rec_pin
        self.rec_mobile = rec_mobile
        self.weight_gram = weight_gram
        self.contents = contents
        self.delivery_type = delivery_type
        self.packing = packing
        self.pickup_time = pickup_time
        self.dropoff_time = dropoff_time
        self.service_cost = service_cost
        self.payment_time = payment_time
        self.status = status

    def from_row(self, r):
        self.booking_id = r["Booking_ID"]
        self.user_id = r["User_ID"]
        self.rec_name = r["Rec_Name"]
        self.rec_address = r["Rec_Address"]
        self.rec_pin = r["Rec_Pin"]
        self.rec_mobile = r["Rec_Mobile"]
        self.weight_gram = r["Par_Weight_Gram"]
        self.contents = r["Par_Contents_Description"]
        self.delivery_type = r["Par_Delivery_Type"]
        self.packing = r["Par_Packing_Preference"]
        self.pickup_time = r["Par_PickupTime"]
        self.dropoff_time = r["Par_DropoffTime"]
        self.service_cost = r["Par_ServiceCost"]
        self.payment_time = r["Par_PaymentTime"]
        self.status = r["Par_Status"]
        return self
