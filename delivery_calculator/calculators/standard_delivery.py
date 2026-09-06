from parcel import Parcel


class StandardDelivery:
    def calculate_delivery_cost(self, parcel: Parcel) -> float:
        weight_factor = 2.0
        return weight_factor * parcel.weight
