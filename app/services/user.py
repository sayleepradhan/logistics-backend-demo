
from bcrypt import checkpw, gensalt, hashpw
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.services.base import BaseService
from app.services.utils import generate_access_token


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession):
        self.model = model
        self.session = session

    async def _add_user(self, data: dict):
        user = self.model(
            **data,
            password_hash = hashpw(
                data["password"].encode("utf-8"),
                gensalt()
            ).decode("utf-8")
        )
        return await self._add(user)

    
    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )
    
    async def _generate_token(self, email, password) -> str:
        # Validate the credentials
        user = await self._get_by_email(email)

        if user is None or not checkpw(
            password.encode("utf-8"), 
            user.password_hash.encode("utf-8")
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect"
            )

        return generate_access_token(
            data= {
                    "user": {
                        "name": user.name,
                        "id": str(user.id)
                    }
                },
        )

    