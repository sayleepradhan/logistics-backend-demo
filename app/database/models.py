from datetime import datetime
from enum import Enum
from random import randint
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import ARRAY, INTEGER
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
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
    status: ShipmentStatus = Field(
            sa_column=Column(
            PgEnum(ShipmentStatus, name='shipmentstatus', create_type=False),
            nullable=False
        )
    )
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy":"selectin"}
    )
    delivery_partner_id: UUID = Field(foreign_key="delivery_partner.id")
    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={ "lazy": "selectin" }
    )

    created_at: datetime = Field(
        sa_column = Column(
            postgresql.TIMESTAMP,
            default = datetime.now()
        )
    )

class User(SQLModel):
    name: str

    email: EmailStr
    password_hash: str = Field(exclude=True)

class Seller(User, table=True):
    __tablename__ = "seller"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )
    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy":"selectin"}
    )

    created_at: datetime = Field(
        sa_column = Column(
            postgresql.TIMESTAMP,
            default = datetime.now()
        )
    )

class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True
        )
    )

    created_at: datetime = Field(
        sa_column = Column(
            postgresql.TIMESTAMP,
            default = datetime.now()
        )
    )

    serviceable_zipcodes: list[int] = Field(
        sa_column = Column(
            ARRAY(INTEGER)
        )
    )
    max_handling_capacity: int
    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={ "lazy": "selectin" }
    )
