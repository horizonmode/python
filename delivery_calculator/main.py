from shipping_service import ShippingService
from calculators.standard_delivery import StandardDelivery
from calculators.express_delivery import ExpressDelivery
from parcel import Parcel

delivery_calculator = ShippingService(StandardDelivery())
express_delivery_calculator = ShippingService(ExpressDelivery())

parcel = Parcel(weight=3.0, destination="PO76TUB")
standard_delivery_cost = delivery_calculator.quote(parcel)
express_delivery_cost = express_delivery_calculator.quote(parcel)

print(f"Standard delivery cost: {standard_delivery_cost}")
print(f"Express delivery cost: {express_delivery_cost}")
