from datetime import datetime
from enum import Enum
from random import randint
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship, SQLModel


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

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
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    status: ShipmentStatus
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy":"selectin"}
    )

class Seller(SQLModel, table=True):

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    name: str

    email: EmailStr
    password_hash: str
    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy":"selectin"}
    )