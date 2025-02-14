from sqlalchemy.ext.asyncio import AsyncSession

from models import User, AuthDevice, AuthLogs
from schemas.account import DeviceSchema
from services.repo.account import query_role_by_code
from utils.crypt import get_hash_password


class UserResource(object):
    @classmethod
    async def create_user(cls, session: AsyncSession, device_data: DeviceSchema, role_code: str = 'normal'):
        role = await query_role_by_code(session, role_code)

        password_digest = await get_hash_password(device_data.device_id)
        user = User(
            password_digest=password_digest,
            status=User.Status.ENABLE.value,
            gender=User.Gender.UNKNOWN.value,
            language=device_data.language,
            country=device_data.country
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)

        user.roles.append(role)
        user.setattr_user_code(user.id)
        user.setattr_username()

        user_device = AuthDevice(**device_data.model_dump(), user_uuid=user.user_uuid)
        session.add(user_device)

        login_log = AuthLogs(
            user_uuid=user.user_uuid,
            device_id=device_data.device_id,
            role_code=role_code,
            device_name=device_data.device_name,
            os_name=device_data.os_name,
            os_version=device_data.os_version,
            ip_address=device_data.ip_address,
            user_agent=device_data.user_agent,
            isp=device_data.isp,
            country=device_data.country
        )
        session.add(login_log)

        return user.id
