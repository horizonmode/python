from dataclasses import dataclass


@dataclass(frozen=True)
class Parcel:
    weight: float
    destination: str
