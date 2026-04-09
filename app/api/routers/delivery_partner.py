from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import (
    DeliveryPartnerDep,
    DeliveryPartnerServiceDep,
    get_partner_access_token,
)
from app.database.redis import add_jti_to_blacklist
from app.schemas.delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])

### Register a delivery partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(partner: DeliveryPartnerCreate, service: DeliveryPartnerServiceDep):
    return await service.add(partner)


### Update Delivery Partner
@router.post("/", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate, 
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep
):
    return await service.update(
        partner.sqlmodel_update(partner_update)
    )

    

### Login the delivery partner
@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep
):
    token = await service.token(
        request_form.username,
        request_form.password
    )
    return {
        "access_token": token,
        "type": "jwt"
    }

### Logout the delivery partner
@router.get("/logout")
async def logout_delivery_partner(token_data: Annotated[dict, Depends(get_partner_access_token)]):
    add_jti_to_blacklist(token_data["jti"])