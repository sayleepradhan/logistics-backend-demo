from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field

from app.database.models import BaseShipment, ShipmentStatus


class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)