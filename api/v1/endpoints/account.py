from fastapi import APIRouter
from fastapi import Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core.dependencies import get_current_user
from core.response import StandardJSONResponse
from core.utils.translation import ugettext_lazy as _
from db.async_engine import get_async_session
from models import User
from schemas.account import DeviceSchema
from schemas.account import UserSchema
from services.account import UserResource
from services.repo.account import query_auth_device
from services.repo.account import query_user_by_user_uuid
from utils import constants
from utils import signature
from utils import stat_code
from utils.geoip import geoip_service
from utils.identifier import custom_identifier

account_router = APIRouter()


@account_router.post(
    "/device",
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))],
    summary="新设备注册登录",
)
async def install_device(
    request: Request, device_data: DeviceSchema, session: AsyncSession = Depends(get_async_session)
):
    # 查询设备是否已注册过，带包名查
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    ip_address = x_forwarded_for if x_forwarded_for != "" else request.client.host
    user_agent = request.headers.get("User-Agent", "")
    ip_info = geoip_service.get_country(ip_address)
    isp = ip_info.get("isp", "")
    country_list = [country.value for country in constants.OpenCountry]
    if ip_info.get("country") not in country_list:
        ip_info["country"] = constants.OpenCountry.PHILIPPINES.value
    ip_info.update({"ip_address": ip_address, "user_agent": user_agent, "isp": isp})
    device_data = DeviceSchema(**device_data.model_dump(), **ip_info)

    auth_device = await query_auth_device(session, device_data.device_id, device_data.package_name)
    if not auth_device:
        user = await UserResource.create_user(session, device_data)
    else:
        user = await query_user_by_user_uuid(session, user_uuid=auth_device.user_uuid)
        if user.status == User.Status.DISABLE.value:
            return StandardJSONResponse(stat_code.USER_IS_DISABLE, _("User is disable"))

    token = signature.create_access_token(user.id)

    return StandardJSONResponse(stat_code.SUCCESS, data={"token": token})


@account_router.get(
    "/me",
    dependencies=[Depends(RateLimiter(times=1, seconds=10, identifier=custom_identifier))],
    summary="获取当前用户信息",
)
async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user()),
):
    data = UserSchema.model_validate(current_user, context={"request": request})

    return StandardJSONResponse(stat_code.SUCCESS, data=data)
