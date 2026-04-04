from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered" 

class Seller(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    name: str

    email: EmailStr
    password_hash: str