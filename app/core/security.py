from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from app.services.utils import decode_access_token

oauth2_scheme_seller =OAuth2PasswordBearer("/seller/token")
oauth2_scheme_delivery_partner =OAuth2PasswordBearer("/partner/token")

class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request):
        auth_credentials = await super().__call__(request)
        token = auth_credentials.credentials

        token_data = decode_access_token(token)

        if token_data is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized"
        )

        return token_data

access_token_bearer = AccessTokenBearer()

Annotated[dict, Depends(access_token_bearer)]