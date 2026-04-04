from datetime import datetime, timedelta

import jwt
from bcrypt import checkpw, gensalt, hashpw
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import security_settings
from app.database.models import Seller
from app.schemas.seller import SellerCreate


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, credentials: SellerCreate):
        seller = Seller(
            **credentials.model_dump(exclude={"password"}),
            # Hashed password
            password_hash=hashpw(
                credentials.password.encode("utf-8"),
                gensalt()
            ).decode("utf-8")
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller

    async def token(self, email, password) -> str:
        # Validate the credentials
        result = await self.session.execute (
            select(Seller).where(Seller.email == email)
        )
        seller = result.scalar()

        if seller is None or checkpw(
            password.encode("utf-8"), 
            seller.password_hash.encode("utf-8")
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect"
            )

        token = jwt.encode(
            payload = {
                "user": {
                    "name": seller.name,
                    "email": seller.email
                },
                "exp" : datetime.now() + timedelta(days=1)
            },
            algorithm = security_settings.JWT_ALGORITHM,
            key = security_settings.JWT_SECRET
        )
        return token
