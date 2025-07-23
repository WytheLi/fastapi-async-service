from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.message import DBMessage
from schemas.messages import MessageCreate


class MessageRepository:
    """消息数据访问层"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(self, message: MessageCreate) -> DBMessage:
        """创建消息"""
        db_message = DBMessage(
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            content=message.content,
            message_type=message.message_type,
            meta=str(message.meta) if message.meta else "{}",
        )
        self.session.add(db_message)
        await self.session.commit()
        await self.session.refresh(db_message)
        return db_message

    async def get_message(self, message_id: str) -> DBMessage | None:
        """获取单个消息"""
        query = await self.session.execute(select(DBMessage).where(DBMessage.id == message_id))
        return query.scalars().first()

    async def mark_as_read(self, message_id: str) -> bool:
        """标记消息为已读"""
        message = await self.get_message(message_id)
        if message:
            message.is_read = True
            await self.session.commit()
            return True
        return False

    async def get_user_messages(self, user_id: str, unread_only: bool = False) -> list[DBMessage]:
        """获取用户消息"""
        stmt = select(DBMessage).where(DBMessage.receiver_id == user_id)
        if unread_only:
            stmt = stmt.where(DBMessage.is_read.is_(False))

        stmt = stmt.order_by(DBMessage.created_at.desc())

        query = await self.session.execute(stmt)
        return query.scalars().all()

    async def delete_message(self, message_id: str) -> bool:
        """删除消息"""
        message = await self.get_message(message_id)
        if message:
            await self.session.delete(message)
            await self.session.commit()
            return True
        return False
