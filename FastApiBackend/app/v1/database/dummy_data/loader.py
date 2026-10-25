from pydantic import EmailStr
from sqlmodel import select
from app.core.db import async_session
from datetime import date
from app.v1.database.dummy_data.data import DummyUserData
from app.v1.database.models.user_model import UserV1
from app.v1.database.models.profile_model import ProfileV1
from app.v1.database.models.education_model import EducationV1
from app.v1.database.models.experience_model import ExperienceV1
from app.v1.database.models.language_model import LanguageV1
from app.v1.database.models.certification_model import CertificationV1

from app.v1.database.models.referee_model import RefereeV1
from app.v1.database.models.project_model import ProjectV1
from app.v1.database.models.verification_model import VerificationV1


class LoadDummyData(DummyUserData):
    def __init__(
        self, user_id: int, dummy_email: EmailStr, dummy_phone_number: str
    ) -> None:
        super().__init__(
            user_id=user_id,
            dummy_email=dummy_email,
            dummy_phone_number=dummy_phone_number,
        )

    async def create_user(self) -> str:
        """Seed the user and every related table, filling only what is still missing."""
        async with async_session() as session:
            created = []

            if not await session.get(UserV1, self.user_id):
                # The user row must exist first; everything else references it.
                session.add(UserV1.model_validate(self.dummy_user))
                await session.commit()
                created.append("user")

            related = (
                (ProfileV1, (self.dummy_profile,)),
                (EducationV1, (self.dummy_education_1, self.dummy_education_2)),
                (ExperienceV1, (self.dummy_experience_1, self.dummy_experience_2)),
                (ProjectV1, (self.dummy_project_1, self.dummy_project_2)),
                (
                    LanguageV1,
                    (
                        self.dummy_language_1,
                        self.dummy_language_2,
                        self.dummy_language_3,
                        self.dummy_language_4,
                    ),
                ),
                (CertificationV1, (self.dummy_certification_1, self.dummy_certification_2)),
                (RefereeV1, (self.dummy_referee_1, self.dummy_referee_2)),
                (VerificationV1, (self.dummy_verification,)),
            )
            for model, items in related:
                has_rows = (
                    await session.exec(
                        select(model).where(model.user_id == self.user_id).limit(1)
                    )
                ).first()
                if has_rows:
                    continue
                session.add_all(model.model_validate(item) for item in items)
                created.append(model.__tablename__)
            await session.commit()

        if not created:
            return f"Dummy data for user_id {self.user_id} already complete"
        return f"Dummy data for user_id {self.user_id} seeded: {', '.join(created)}"
