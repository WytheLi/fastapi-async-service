from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import AuthDevice, Role, User


async def query_auth_device(session: AsyncSession, device_id: str, package_name: str):
    query = await session.execute(
        select(AuthDevice).where(AuthDevice.device_id == device_id, AuthDevice.package_name == package_name)
    )
    return query.scalars().first()


async def query_user_by_user_uuid(session: AsyncSession, user_uuid: str):
    query = await session.execute(
        select(User).where(User.user_uuid == user_uuid, User.is_delete.is_(False))
    )
    return query.scalars().first()


async def query_user_by_user_id(session: AsyncSession, user_id: int):
    query = await session.execute(
        select(User).where(User.id == user_id, User.is_delete.is_(False))
    )
    return query.scalars().first()


async def query_role_by_code(session: AsyncSession, role_code: str):
    query = await session.execute(
        select(Role).where(Role.role_code == role_code)
    )
    return query.scalars().first()
