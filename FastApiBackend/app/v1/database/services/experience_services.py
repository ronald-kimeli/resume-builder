from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from app.v1.database.services.user_services import UserCRUDService
from typing import List
from app.v1.database.models.experience_model import (
    ExperienceV1,
    ExperienceV1Create,
    ExperienceV1CreateRequest,
    ExperienceV1Read,
    ExperienceV1Update,
)


class ExperienceCRUDServices(UserCRUDService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)

    async def read_user_experience_details(self, user_id: int) -> List[ExperienceV1Read]:
        user = await self.get_user(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not Found")
        else:
            return user.experience_details

    async def create_user_experience(
        self, user_id: int, user_experience_request: ExperienceV1CreateRequest
    ) -> ExperienceV1Read:
        user = await self.get_user(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not Found")
        else:
            user_experience = ExperienceV1Create.model_validate(user_experience_request)
            user_experience.user_id = user_id
            user_experience_db_create = ExperienceV1.model_validate(user_experience)

            self.session.add(user_experience_db_create)
            await self.session.commit()
            await self.session.refresh(user_experience_db_create)

            return user_experience_db_create

    async def update_user_experience(
        self, user_id: int, experience_id: int, experience: ExperienceV1Update
    ) -> ExperienceV1Read:
        user_experience = (await self.session.exec(
            select(ExperienceV1).where(
                ExperienceV1.user_id == user_id,
                ExperienceV1.experience_id == experience_id,
            )
        )).one_or_none()

        if user_experience is None:
            raise HTTPException(status_code=404, detail="User Experience Not Found")
        else:
            new_user_experience = experience.model_dump(exclude_none=True)
            for key, value in new_user_experience.items():
                setattr(user_experience, key, value)

            self.session.add(user_experience)
            await self.session.commit()
            await self.session.refresh(user_experience)

            return user_experience

    async def delete_user_experience(
        self, user_id: int, experience_id: int
    ) -> ExperienceV1Read:
        user_experience = (await self.session.exec(
            select(ExperienceV1).where(
                ExperienceV1.user_id == user_id,
                ExperienceV1.experience_id == experience_id,
            )
        )).one_or_none()

        if user_experience is None:
            raise HTTPException(status_code=404, detail="User Experience Not Found")
        else:
            await self.session.delete(user_experience)
            await self.session.commit()

            return {"Status": "Successfully deleted"}
