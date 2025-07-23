from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from .basis import BaseModel


class DBMessage(BaseModel):
    """数据库消息模型"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(String(50), index=True)
    receiver_id = Column(String(50), index=True)
    content = Column(Text)
    message_type = Column(String(20), default="notification")
    is_read = Column(Boolean, default=False)
    meta = Column(Text, default="{}")  # 存储为JSON字符串
