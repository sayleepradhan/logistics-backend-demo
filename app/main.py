from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from contextlib import asynccontextmanager

from .schemas import Shipment
from .database import Database
from app.database.session import create_db_tables

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield
app = FastAPI()

db = Database()

@app.get("/shipment")
def get_shipment(id: int | None = None) -> Shipment:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist"
            )
    return shipment

@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> dict[str, Any]:
    new_id = db.create(shipment)
    return {"id": new_id}

@app.patch("/shipment/")
def update_shipment(shipment: Shipment) -> dict[str, Any]:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Given id doesn't exist"
            )
    
    updated_shipment = db.update(id, Shipment)
    return updated_shipment

@app.delete("/shipment/")
def delete_shipment(id: int) -> dict[str, Any]:
    db.delete(id)
    return {"detail": f"Shipment with id {id} is deleted."}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url = app.openapi_url,
        title = "Scalar API",
    )