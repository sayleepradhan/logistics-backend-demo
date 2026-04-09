from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import oauth2_scheme_delivery_partner, oauth2_scheme_seller
from app.database.models import DeliveryPartner, Seller
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.delivery_partner import DeliveryPartnerService
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.services.utils import decode_access_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_shipment_service(session: SessionDep, partner: "DeliveryPartnerServiceDep"):
    return ShipmentService(session, partner)

ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

async def _get_access_token(token: str):
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Access Token"
        )
    return data

async def get_seller_access_token(token: Annotated[str, Depends(oauth2_scheme_seller)]):
    return await _get_access_token(token)

async def get_partner_access_token(token: Annotated[str, Depends(oauth2_scheme_delivery_partner)]):
    return await _get_access_token(token)

async def get_current_seller(
        token_data: Annotated[dict, Depends(get_seller_access_token)],
        session: SessionDep
):
    seller =  await session.get(Seller, UUID(token_data["user"]["id"]))
    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found"
        )
    return seller

SellerDep = Annotated[Seller, Depends(get_current_seller)]

def get_seller_service(session: SessionDep):
    return SellerService(session)

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

async def get_current_partner(
        token_data: Annotated[dict, Depends(get_partner_access_token)],
        session: SessionDep
):
    partner = await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))
    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery Partner not found"
        )
    return partner

DeliveryPartnerDep = Annotated[Seller, Depends(get_current_partner)]

def get_partner_service(session: SessionDep):
    return DeliveryPartnerService(session)

DeliveryPartnerServiceDep = Annotated[DeliveryPartnerService, Depends(get_partner_service)]
