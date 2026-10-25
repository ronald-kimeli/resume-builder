import asyncio
import re
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# imports below are essential in loading version 1 models to avoid circular import error
from app.v1.database.models.user_model import UserV1
from app.v1.database.models.profile_model import ProfileV1
from app.v1.database.models.project_model import ProjectV1
from app.v1.database.models.language_model import LanguageV1
from app.v1.database.models.education_model import EducationV1
from app.v1.database.models.experience_model import ExperienceV1
from app.v1.database.models.referee_model import RefereeV1
from app.v1.database.models.certification_model import CertificationV1
from app.v1.database.models.verification_model import VerificationV1
from app.v1.database.models.health_status_model import HealthCheck

from app import settings
from app.core.db import initialize_db
from app.core.events import publisher
from app.v1 import v1_router
from app.v1.database.dummy_data.loader import LoadDummyData

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ALEMBIC_CONFIG_FILE = BASE_DIR / "alembic.ini"

DUMMY_USERS = (
    (1, "test_email_1@email.com", "+254711215654"),
    (2, "test_email_2@email.com", "+254711217654"),
    (3, "test_email_3@email.com", "+254712215654"),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_db()
    # seed sequentially so the unique email/phone constraints never race
    for user_id, email, phone in DUMMY_USERS:
        print(
            await LoadDummyData(
                user_id=user_id, dummy_email=email, dummy_phone_number=phone
            ).create_user()
        )
    yield
    await publisher.close()


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1_router.v1_router)

# /api/v1/user/{id}/<anything> mutations change that user's resume data
_USER_RESUME_PATH = re.compile(rf"^{re.escape(v1_router.v1_router.prefix)}/user/(\d+)/")
_background: set[asyncio.Task] = set()  # strong refs so tasks aren't garbage-collected
_MUTATING = {"POST", "PUT", "PATCH", "DELETE"}


@app.middleware("http")
async def notify_resume_change(request: Request, call_next):
    response = await call_next(request)
    if request.method in _MUTATING and response.status_code < 400:
        match = _USER_RESUME_PATH.match(request.url.path)
        if match:
            user_id = int(match.group(1))
            # fire-and-forget: never delay the HTTP response for the broker
            task = asyncio.create_task(
                publisher.publish(
                    user_id,
                    {
                        "event": "resume.updated",
                        "user_id": user_id,
                        "method": request.method,
                        "path": request.url.path,
                    },
                )
            )
            _background.add(task)
            task.add_done_callback(_background.discard)
    return response


@app.get("/", response_model=HealthCheck, tags=["Status"])
async def health_check() -> dict:
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
    }
