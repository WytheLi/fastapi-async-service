import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from core.websocket.websocket_manager import manager
from db.async_engine import get_async_session
from schemas.messages import WebSocketMessage
from services.message import MessageService
from services.repo.message import MessageRepository

router = APIRouter()


@router.websocket("/messages/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, session: AsyncSession = Depends(get_async_session)):
    """WebSocket消息推送端点"""
    # 用户连接
    await manager.connect(user_id, websocket)

    try:
        # 连接建立后立即发送所有未读消息
        repo = MessageRepository(session)
        service = MessageService(repo)
        unread_messages = await service.get_user_unread_messages(user_id)

        for msg in unread_messages:
            ws_msg = WebSocketMessage(action="new_message", data=msg.model_dump())
            await websocket.send_text(ws_msg.model_dump_json())

        # 保持连接活跃
        while True:
            data = await websocket.receive_text()

            # 忽略心跳消息
            if data == "pong":
                continue

            try:
                message = json.loads(data)
                action = message.get("action")

                if action == "mark_read":
                    # 标记消息为已读
                    message_id = message.get("message_id")
                    if message_id:
                        if await service.mark_message_as_read(message_id):
                            # 发送确认
                            ws_msg = WebSocketMessage(action="mark_read_success", data={"message_id": message_id})
                            await websocket.send_text(ws_msg.model_dump_json())

                elif action == "delete":
                    # 删除消息
                    message_id = message.get("message_id")
                    if message_id:
                        if await service.delete_message(message_id):
                            # 发送确认
                            ws_msg = WebSocketMessage(action="delete_success", data={"message_id": message_id})
                            await websocket.send_text(ws_msg.model_dump_json())

            except json.JSONDecodeError:
                # 发送错误消息
                ws_msg = WebSocketMessage(action="error", data={"error": "Invalid JSON format"})
                await websocket.send_text(ws_msg.model_dump_json())

    except WebSocketDisconnect:
        # 处理连接断开
        manager.disconnect(websocket)
