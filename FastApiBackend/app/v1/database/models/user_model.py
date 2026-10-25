from pydantic import ConfigDict
from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
import phonenumbers

if TYPE_CHECKING:
    from app.v1.database.models.language_model import LanguageV1
    from app.v1.database.models.education_model import EducationV1
    from app.v1.database.models.experience_model import ExperienceV1
    from app.v1.database.models.project_model import ProjectV1
    from app.v1.database.models.profile_model import ProfileV1
    from app.v1.database.models.certification_model import CertificationV1
    from app.v1.database.models.referee_model import RefereeV1
    from app.v1.database.models.verification_model import VerificationV1


# The class `UserV1Base` represents a user with attributes such as name, password, and email.
class UserV1Base(SQLModel):
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(index=True, nullable=False)
    phone_number: str = Field(index=True, nullable=False, unique=True)

    @field_validator("phone_number")
    @classmethod
    def phone_number_is_valid_number(cls, v):
        try:
            phone_number = phonenumbers.parse(v, None)
        except phonenumbers.NumberParseException:
            raise ValueError("Potentially Not a valid Phone Number")

        if phonenumbers.is_valid_number(phone_number):
            return v
        else:
            raise ValueError("Not a valid Phone Number")

    @field_validator("phone_number")
    @classmethod
    def phone_number_starts_with_country_code(cls, v: str):
        if v.startswith("+"):
            return v
        else:
            raise ValueError("Phone Number should start with country code")


# The UserV1 class represents a user with various details such as education, experience, language,
# projects, and contact information.
class UserV1(UserV1Base, table=True):
    user_id: int = Field(default=None, primary_key=True)
    education_details: List["EducationV1"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    experience_details: List["ExperienceV1"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    language_details: List["LanguageV1"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    project_details: List["ProjectV1"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    profile_details: List["ProfileV1"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    certification_details: List["CertificationV1"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    referee_details: List["RefereeV1"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    verification_details: List["VerificationV1"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )


# The `UserV1Create` class is a subclass of `UserV1Base` and includes a `Config` class with an `example`
# attribute that provides an example JSON schema for creating a user.
class UserV1Create(UserV1Base):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "test_email_1@email.com",
            "password": "test_password",
            "phone_number": "+254712365478",
        }
    })

# The `UserV1Read` class is a subclass of `UserV1Base` that includes a `user_id` attribute and a `Config`
# class with an example schema.
class UserV1Read(UserV1Base):
    user_id: int

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "test_email_1@email.com",
            "password": "test_password",
            "phone_number": "+254712365478",
            "user_id": "user_id",
        }
    })

# The `UserV1Update` class is a subclass of `UserV1Base` that allows for updating user information such as
# name and password.
class UserV1Update(UserV1Base):
    name: Optional[str] = None
    password: Optional[str] = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "test_email_1@email.com",
            "password": "test_password",
            "phone_number": "+254712365478"
            # "user_id": "User_id",
        }
    })
