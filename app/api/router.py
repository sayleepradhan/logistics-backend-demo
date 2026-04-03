from typing import Any

from fastapi import APIRouter

from app.database.session import SessionDep
from app.schemas.shipment import Shipment, ShipmentCreate, ShipmentUpdate
from app.service.shipment import ShipmentService

router = APIRouter()

@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, session: SessionDep):
    return await ShipmentService(session).get(id)

@router.post("/shipment", response_model=None)
async def submit_shipment(shipment: ShipmentCreate, session: SessionDep):
    new_shipment = await ShipmentService(session).add(shipment)
    return {"id": new_shipment.id}

@router.patch("/shipment/", response_model=Shipment)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    return await ShipmentService(session).update(shipment_update)

@router.delete("/shipment/")
async def delete_shipment(id: int, session: SessionDep) -> dict[str, Any]:
    await ShipmentService(session).delete(id)
    return {"detail": f"Shipment with id {id} is deleted."}
