from fastapi import APIRouter

from app.api.routers import seller, shipment

master_router = APIRouter()

master_router.include_router(shipment.router)
master_router.include_router(seller.router)