from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core.response import CustomJSONResponse
from db.async_engine import get_async_session
from infrastructure.kafka.producer import kafka_producer
from schemas.analysis import UserActivitySchema
from services.builders.constants import EventType
from settings import settings
from utils.status_info import StatusInfo

analysis_router = APIRouter()


@analysis_router.post("/user_activity", summary='用户行为数据')
async def user_activity_write(
        request: Request,
        activity_data: UserActivitySchema,
        session: AsyncSession = Depends(get_async_session)
):
    data = {
        "event_type": EventType.USER_ACTIVITY.value,
        "content": activity_data.model_dump()
    }
    await kafka_producer.send_message(settings.KAFKA_TOPIC, data)
    return CustomJSONResponse(StatusInfo.Success)
