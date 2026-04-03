from typing import Annotated

from app.service.shipment import ShipmentService
from app.database.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_shipment_service(session: SessionDep):
    return ShipmentService(session)

ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
