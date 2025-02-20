from loguru import logger

from db.async_engine import async_session
from models import UserActivityLog
from services import builders
from services.builders import BaseEventHandler
from services.builders.constants import EventType


@builders.BuilderFactory.register(EventType.USER_ACTIVITY.value)
class UserActivityEventHandler(BaseEventHandler):
    """ 处理用户行为数据写入 """
    async def handle(self, content: dict):
        async with async_session() as session:
            try:
                activity_record = UserActivityLog(**content)
                session.add(activity_record)
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Error saving user activity: {e}")
