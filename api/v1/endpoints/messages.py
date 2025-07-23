import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.websocket.websocket_manager import manager
from db.async_engine import get_async_session
from schemas.messages import Message
from schemas.messages import MessageCreate
from schemas.messages import WebSocketMessage
from services.message import MessageService
from services.repo.message import MessageRepository

router = APIRouter()


@router.post("", response_model=Message)
async def send_message(message_data: MessageCreate, session: AsyncSession = Depends(get_async_session)) -> Message:
    """发送新消息"""
    repo = MessageRepository(session)
    service = MessageService(repo)

    message = await service.send_message(message_data)

    # 通过WebSocket实时推送给接收者
    ws_msg = WebSocketMessage(action="new_message", data=message.model_dump())
    await manager.send_personal_message(json.dumps(ws_msg.model_dump()), message.receiver_id)

    return message


@router.post("/{message_id}/read")
async def mark_message_as_read(message_id: str, session: AsyncSession = Depends(get_async_session)) -> dict:
    """标记消息为已读"""
    repo = MessageRepository(session)
    service = MessageService(repo)

    if await service.mark_message_as_read(message_id):
        return {"status": "success", "message": "Message marked as read"}
    raise HTTPException(status_code=404, detail="Message not found")


@router.get("/{user_id}/unread", response_model=list[Message])
async def get_unread_messages(user_id: str, session: AsyncSession = Depends(get_async_session)) -> list[Message]:
    """获取用户未读消息"""
    repo = MessageRepository(session)
    service = MessageService(repo)

    return await service.get_user_unread_messages(user_id)


@router.delete("/{message_id}")
async def delete_message(message_id: str, session: AsyncSession = Depends(get_async_session)) -> dict:
    """删除消息"""
    repo = MessageRepository(session)
    service = MessageService(repo)

    if await service.delete_message(message_id):
        return {"status": "success", "message": "Message deleted"}
    raise HTTPException(status_code=404, detail="Message not found")
