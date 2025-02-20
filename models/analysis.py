from sqlalchemy import Column, Integer, String, JSON

from models import BaseModel


class UserActivityLog(BaseModel):
    """ 用户行为埋点数据 """
    __tablename__ = 'user_activity_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(String(255), nullable=False)
    package_name = Column(String(255), nullable=False)
    content = Column(JSON, comment="埋点数据")
