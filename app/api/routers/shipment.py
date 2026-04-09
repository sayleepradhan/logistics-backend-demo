from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import SellerDep, ShipmentServiceDep
from app.database.models import Shipment
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate

router = APIRouter(tags=["Shipment"])

@router.get("/shipment", response_model=Shipment)
async def get_shipment(
    id: UUID,
    service: ShipmentServiceDep,
    seller: SellerDep
):
    return await service.get(id)

@router.post("/shipment", response_model=None)
async def submit_shipment(
    seller: SellerDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep
):
    return await service.add(shipment, seller)

@router.patch("/shipment/", response_model=Shipment)
async def update_shipment(id: UUID, shipment_update: ShipmentUpdate, service: ShipmentServiceDep):
    update = shipment_update.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "No data provided to update"
        )

    return await service.update(id, update)

@router.delete("/shipment/")
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, Any]:
    await service.delete(id)
    return {"detail": f"Shipment with id {id} is deleted."}
