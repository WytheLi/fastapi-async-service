from typing import Any
from typing import Dict

from pydantic import BaseModel
from pydantic import Field


class MessageBase(BaseModel):
    """消息基础模型"""

    receiver_id: str = Field(..., description="接收者ID")
    content: str = Field(..., max_length=1000, description="消息内容")
    message_type: str = Field("notification", description="消息类型: notification/alert/private")
    meta: Dict[str, Any] = Field(None, description="附加元数据")


class MessageCreate(MessageBase):
    """创建消息模型"""

    sender_id: str = Field(..., description="发送者ID")


class Message(MessageBase):
    """完整消息模型"""

    id: int = Field(..., description="消息ID")
    sender_id: str = Field(..., description="发送者ID")
    is_read: bool = Field(False, description="是否已读")
    # created_at: datetime = Field(..., description="创建时间")
    meta: str = Field(..., description="附加元数据")

    class Config:
        from_attributes = True


class WebSocketMessage(BaseModel):
    """WebSocket消息格式"""

    action: str  # "new_message", "mark_read", "delete_message", "error"
    data: Any
