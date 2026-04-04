from bcrypt import gensalt, hashpw
from sqlalchemy.ext.asyncio import AsyncSession

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
