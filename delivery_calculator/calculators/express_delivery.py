from parcel import Parcel


class ExpressDelivery:
    def calculate_delivery_cost(self, parcel: Parcel) -> float:
        weight_factor = 5.0
        express_extra = 10
        return weight_factor * parcel.weight + express_extra
