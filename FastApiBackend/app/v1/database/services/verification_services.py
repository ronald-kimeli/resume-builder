from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
import africastalking
import asyncio
import pyotp, datetime
from app.v1.database.models.verification_model import (
    VerificationV1,
    VerificationV1Create,
)
from app import settings


class CreateVerificationDetails:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def generate_time_based_otp(self) -> int:
        otp_generator = pyotp.TOTP(s="U2ERQTKVMK7KKDJQSVS5T4LEK57VB24V", interval=1)
        return int(otp_generator.now())

    async def send_otp_to_number(self, otp_code: int, phone_number: List[str]):
        # The Africa's Talking SDK is blocking, so run it in a worker thread
        # to keep the event loop free for other requests.
        def _send() -> dict:
            africastalking.initialize(
                settings.africas_talking_username, settings.africas_talking_api_key
            )
            return africastalking.SMS.send(
                f"Your OTP code is {otp_code} for Number: {phone_number}",
                [settings.test_phone_number],
            )

        print(await asyncio.to_thread(_send))

    async def create_phone_number_verification_details(self, user_id: int) -> int:
        otp_code = self.generate_time_based_otp()
        otp_created_at = datetime.datetime.now(datetime.timezone.utc)
        otp_expiry_at = otp_created_at + datetime.timedelta(minutes=5)

        verification_create = VerificationV1Create(
            otp_code=otp_code,
            otp_created_at=otp_created_at,
            otp_expiry_at=otp_expiry_at,
            number_verified=False,
            user_id=user_id,
        )

        verification_instance = VerificationV1.model_validate(verification_create)
        self.session.add(verification_instance)
        await self.session.commit()
        await self.session.refresh(verification_instance)

        return otp_code

    async def update_phone_verified_field(self, user_id: int) -> bool:
        verification_instance = (await self.session.exec(
            select(VerificationV1).where(VerificationV1.user_id == user_id)
        )).one_or_none()

        verification_instance.number_verified = True

        self.session.add(verification_instance)
        await self.session.commit()
        await self.session.refresh(verification_instance)

        return True

        pass
