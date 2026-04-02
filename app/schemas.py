from datetime import datetime
from random import randint

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from app.database.models import ShipmentStatus


def random_destination():
    return randint(11000, 99999)

class BaseShipment(SQLModel):
    content: str = Field(
        description="Shipment content",
        max_length=100
    )
    weight: float = Field(
        description="Shipment weight",
        ge=0.25
    )
    destination: int | None = Field(
        description="Shipment destination. If not provided will generate a random destination",
        default_factory=random_destination
    )


class Shipment(BaseShipment, table=True):
    id: int = Field(default=None, primary_key=True)
    status: ShipmentStatus
    estimated_delivery: datetime

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)