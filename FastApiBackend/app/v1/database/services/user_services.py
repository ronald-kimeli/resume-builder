from fastapi import HTTPException
from app.v1.database.models.user_model import (
    UserV1,
    UserV1Update,
    UserV1Read,
    UserV1Create,
)
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import EmailStr
from typing import Optional
from app.v1.database.services.user_services_helper_functions import get_full_profile
from app.v1.database.services.verification_services import CreateVerificationDetails


class UserCRUDService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def email_exists(self, email: EmailStr) -> bool:
        if (await self.session.exec(select(UserV1).where(UserV1.email == email))).one_or_none():
            return True
        else:
            return False

    async def user_id_exists(self, user_id: int) -> bool:
        if (await self.session.exec(
            select(UserV1).where(UserV1.user_id == user_id)
        )).one_or_none():
            return True
        else:
            return False

    async def phone_number_exists(self, phone_number: str) -> bool:
        if (await self.session.exec(
            select(UserV1).where(UserV1.phone_number == phone_number)
        )).one_or_none():
            return True
        else:
            return False

    async def get_user(
        self, email: Optional[EmailStr] = None, user_id: Optional[int] = None
    ) -> UserV1 | None:
        # if both email and user_id are not provided raise error
        if email is None and user_id is None:
            raise HTTPException(
                status_code=401, detail="Please provide either a user_id or an email"
            )

        # if email is provided and it exists in the db return user
        if email:
            if await self.email_exists(email=email):
                return (await self.session.exec(
                    select(UserV1).where(UserV1.email == email)
                )).one_or_none()
        # if user_id is provided and it exists in db return user
        elif user_id:
            if await self.user_id_exists(user_id=user_id):
                return (await self.session.exec(
                    select(UserV1).where(UserV1.user_id == user_id)
                )).one_or_none()
        # if no user found return None
        return None

    async def create_user(self, new_user: UserV1Create) -> UserV1Read | dict:
        email_exists = await self.email_exists(email=new_user.email)
        phone_number_exists = await self.phone_number_exists(
            phone_number=new_user.phone_number
        )
        credentials_exist = {
            "Email Exists": False,
            "Phone Number Exists": False,
        }

        if email_exists and phone_number_exists:
            credentials_exist["Email Exists"] = True
            credentials_exist["Phone Number Exists"] = True
            raise HTTPException(status_code=409, detail=credentials_exist)

        elif email_exists:
            credentials_exist["Email Exists"] = True
            raise HTTPException(status_code=409, detail=credentials_exist)

        elif phone_number_exists:
            credentials_exist["Phone Number Exists"] = True
            raise HTTPException(status_code=409, detail=credentials_exist)

        else:
            new_user_instance = UserV1.model_validate(new_user)
            # new_user_instance = UserV1.model_validate(new_user)
            self.session.add(new_user_instance)
            await self.session.commit()
            await self.session.refresh(new_user_instance)

            create_verification_details_service = CreateVerificationDetails(
                session=self.session
            )
            otp_code = await create_verification_details_service.create_phone_number_verification_details(
                user_id=new_user_instance.user_id
            )

            if otp_code:
                await create_verification_details_service.send_otp_to_number(
                    otp_code=otp_code, phone_number=new_user_instance.phone_number
                )
                return new_user_instance
            else:
                raise HTTPException(status_code=409, detail="Error generating otp")

    async def update_user(
        self,
        email: Optional[EmailStr] = None,
        user_id: Optional[int] = None,
        new_user: Optional[UserV1Update] = None,
    ):
        # Get user
        user_in_db = await self.get_user(email=email, user_id=user_id)
        if user_in_db is None:
            raise HTTPException(status_code=404, detail="User not Found")
        else:
            # save email to reapply later thus preventing changing of emails
            user_email_from_db = user_in_db.email
            # Sanity checks, If password field is empty set to None
            if new_user.password == "":
                new_user.password = None

            # Sanity checks, If user name field is empty set to None
            if new_user.name == "":
                new_user.name = None

            new_user_data = new_user.model_dump(exclude_none=True)
            for key, value in new_user_data.items():
                setattr(user_in_db, key, value)

            # resetting email to email set before the update
            user_in_db.email = user_email_from_db

            self.session.add(user_in_db)
            await self.session.commit()
            await self.session.refresh(user_in_db)

            return user_in_db

    async def delete_user(
        self, user_id: Optional[int] = None, email: Optional[EmailStr] = None
    ) -> bool | HTTPException:
        user_to_delete = await self.get_user(email=email, user_id=user_id)

        if user_to_delete is None:
            raise HTTPException(status_code=404, detail="User not Found")
        else:
            await self.session.delete(user_to_delete)
            await self.session.commit()

            return True

    # Functions below this comment have their logic encapsulated in functions found in
    # app.v1.database.services.user_services_helper_functions file

    async def get_full_user_details(
        self, user_id: Optional[int] = None, email: Optional[EmailStr] = None
    ) -> dict:
        user = await self.get_user(user_id=user_id, email=email)
        if user is None:
            raise HTTPException(status_code=404, detail="User Not found.")
        else:
            return get_full_profile(user=user)
