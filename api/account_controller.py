from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core.decorators import authorize_required
from utils.identifier import custom_identifier
from db.async_engine import get_async_session
from models import User
from schemas.account import DeviceSchema, UserSchema
from services.repo.account import query_auth_device, query_user_by_user_uuid
from services.account import UserResource
from utils import constants, signature, ip_parse
from core.response import CustomJSONResponse
from utils.status_info import StatusInfo

account_router = APIRouter()


@account_router.post(
    "/device",
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
    summary='新设备注册登录'
)
async def install_device(
        request: Request,
        device_data: DeviceSchema,
        session: AsyncSession = Depends(get_async_session)
):
    # 查询设备是否已注册过，带包名查
    x_forwarded_for = request.headers.get('X-Forwarded-For', '')
    ip_address = x_forwarded_for if x_forwarded_for != '' else request.client.host
    user_agent = request.headers.get('User-Agent', '')
    ip_parse_info = ip_parse.get_cidr_info_with_isp(ip_address)
    isp = ip_parse_info.get('isp', '')
    country_list = [country.value for country in constants.OpenCountry]
    if ip_parse_info["country_name"] not in country_list:
        country = constants.OpenCountry.AMERICA.value
    else:
        country = ip_parse_info["country_name"]
    ip_info = {"ip_address": ip_address, "user_agent": user_agent, 'isp': isp, 'country': country}
    device_data = DeviceSchema(**device_data.model_dump(), **ip_info)

    auth_device = await query_auth_device(session, device_data.device_id, device_data.package_name)
    if not auth_device:
        user_id = await UserResource.create_user(session, device_data)
    else:
        user = await query_user_by_user_uuid(session, user_uuid=auth_device.user_uuid)
        if user.status == User.Status.DISABLE.value:
            return CustomJSONResponse(StatusInfo.USER_IS_DISABLE)
        user_id = user.id

    token = signature.create_access_token(user_id)

    return CustomJSONResponse(StatusInfo.Success, data={"token": token})


@account_router.get(
    "/me",
    dependencies=[Depends(RateLimiter(times=1, seconds=10, identifier=custom_identifier))],
    summary='新设备注册登录'
)
@authorize_required(perms=[])
async def install_device(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    user = request.state.user

    data = UserSchema.model_validate(user, context={"request": request})

    return CustomJSONResponse(StatusInfo.Success, data=data)
