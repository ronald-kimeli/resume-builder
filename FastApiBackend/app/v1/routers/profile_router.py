from fastapi import APIRouter, Depends
from app.core.db import get_db_session
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from app.v1.database.services.profile_services import ProfileCRUDServices
from app.v1.database.models.profile_model import (
    ProfileV1Update,
    ProfileV1Read,
    ProfileV1CreateRequest,
)

router = APIRouter(prefix="/user/{user_id}/profile", tags=["Profile Version 1"])


@router.get("/", response_model=List[ProfileV1Read])
async def read_profile(
    *,
    session: AsyncSession = Depends(get_db_session),
    user_id: int,
):
    profile_crud_service = ProfileCRUDServices(session=session)
    return await profile_crud_service.read_user_profile(user_id=user_id)


@router.post("/", response_model=ProfileV1Read)
async def create_profile(
    *,
    session: AsyncSession = Depends(get_db_session),
    user_id: int,
    profile_request: ProfileV1CreateRequest,
):
    profile_crud_service = ProfileCRUDServices(session=session)
    return await profile_crud_service.create_user_profile(
        user_id=user_id, profile_request=profile_request
    )


@router.patch("/{profile_id}", response_model=ProfileV1Read)
async def update_profile(
    *,
    session: AsyncSession = Depends(get_db_session),
    user_id: int,
    profile_id: int,
    update_profile: ProfileV1Update,
):
    profile_crud_service = ProfileCRUDServices(session=session)
    return await profile_crud_service.update_user_profile(
        user_id=user_id, profile_id=profile_id, update_profile=update_profile
    )


@router.delete("/{profile_id}")
async def delete_profile(
    *, session: AsyncSession = Depends(get_db_session), user_id: int, profile_id: int
):
    profile_crud_service = ProfileCRUDServices(session=session)
    return await profile_crud_service.delete_user_profile(
        user_id=user_id, profile_id=profile_id
    )
