from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.schemas.shipment import Shipment, ShipmentCreate, ShipmentUpdate
from app.api.dependencies import ServiceDep

router = APIRouter()

@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, service: ServiceDep):
    return await service.get(id)

@router.post("/shipment", response_model=None)
async def submit_shipment(shipment: ShipmentCreate, service: ServiceDep):
    new_shipment = await service.add(shipment)
    return {"id": new_shipment.id}

@router.patch("/shipment/", response_model=Shipment)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ServiceDep):
    update = shipment_update.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "No data provided to update"
        )

    return await service.update(id, update)

@router.delete("/shipment/")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, Any]:
    await service.delete(id)
    return {"detail": f"Shipment with id {id} is deleted."}
