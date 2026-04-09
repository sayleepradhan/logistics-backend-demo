from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Seller, Shipment, ShipmentStatus
from app.schemas.shipment import ShipmentCreate
from app.services.base import BaseService
from app.services.delivery_partner import DeliveryPartnerService


class ShipmentService(BaseService):
    def __init__(self, session: AsyncSession, deliveryPartnerService: DeliveryPartnerService):
        super().__init__(Shipment, session)
        self.partnerService = deliveryPartnerService

    async def get(self, id: UUID) -> Shipment | None:
        return await self._get(id)

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status = ShipmentStatus.placed,
            estimated_delivery = datetime.now() + timedelta(days=3),
            seller_id = seller.id
        )
        partner = await self.partnerService.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        return await self._add(new_shipment)

    async def update(self, id: UUID, shipment_update: dict) -> Shipment | None:
        shipment = await self._get(id)
        shipment.sqlmodel_update(shipment_update)

        return await self._update(shipment)

    async def delete(self, id: UUID) -> None:
        shipment = await self._get(id)
        return await self._delete(shipment)