from random import randint

from pydantic import BaseModel, Field

def random_destination():
    return randint(11000, 99999)

class Shipment(BaseModel):
    content: str = Field(
        description="Shipment content",
        max_length=100
    )
    weight: float = Field(
        description="Shipment weight",
        le=25,
        ge=0.5
    )
    id: int = 0
    status: str = "placed"
    destination: int | None = Field(
        description="Shipment destination. If not provided will generate a random destination",
        default_factory=random_destination
    )
