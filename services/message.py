from schemas.messages import Message
from schemas.messages import MessageCreate
from services.repo.message import MessageRepository


class MessageService:
    """消息业务逻辑层"""

    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

    async def send_message(self, message_data: MessageCreate) -> Message:
        """发送消息"""
        db_message = await self.message_repo.create_message(message_data)
        return Message.model_validate(db_message)

    async def get_user_unread_messages(self, user_id: str) -> list[Message]:
        """获取用户未读消息"""
        db_messages = await self.message_repo.get_user_messages(user_id, unread_only=True)
        return [Message.model_validate(msg) for msg in db_messages]

    async def mark_message_as_read(self, message_id: str) -> bool:
        """标记消息为已读"""
        return await self.message_repo.mark_as_read(message_id)

    async def delete_message(self, message_id: str) -> bool:
        """删除消息"""
        return await self.message_repo.delete_message(message_id)
