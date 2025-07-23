import asyncio
from typing import Dict

from starlette.websockets import WebSocket

from settings import settings


class WebSocketManager:
    """WebSocket连接管理器"""

    def __init__(self):
        # 用户ID到WebSocket连接的映射
        self.active_connections: Dict[str, WebSocket] = {}
        # 连接ID到用户ID的映射
        self.connection_user_map: Dict[str, str] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        """用户连接"""
        await websocket.accept()

        # 如果用户已有连接，先关闭旧连接
        if user_id in self.active_connections:
            old_ws = self.active_connections[user_id]
            await old_ws.close(code=1000, reason="New connection from same user")

        # 存储新连接
        self.active_connections[user_id] = websocket
        self.connection_user_map[id(websocket)] = user_id

        # 启动心跳任务
        asyncio.create_task(self.heartbeat(websocket))

    async def heartbeat(self, websocket: WebSocket):
        """连接心跳机制"""
        try:
            while True:
                await asyncio.sleep(settings.WEBSOCKET_TIMEOUT // 2)
                if websocket in self.active_connections.values():
                    await websocket.send_text("ping")
                else:
                    break
        except Exception:
            self.disconnect(websocket)

    def disconnect(self, websocket: WebSocket):
        """断开连接"""
        connection_id = id(websocket)
        if connection_id in self.connection_user_map:
            user_id = self.connection_user_map[connection_id]
            del self.active_connections[user_id]
            del self.connection_user_map[connection_id]

    async def send_personal_message(self, message: str, user_id: str):
        """向特定用户发送消息"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_text(message)
            except Exception:
                self.disconnect(websocket)

    async def broadcast(self, message: str):
        """广播消息（给所有连接的用户）"""
        for user_id, websocket in list(self.active_connections.items()):
            try:
                await websocket.send_text(message)
            except Exception:
                self.disconnect(websocket)


# 全局连接管理器
manager = WebSocketManager()
