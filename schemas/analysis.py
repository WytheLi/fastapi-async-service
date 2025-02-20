from pydantic import BaseModel


class UserActivitySchema(BaseModel):
    user_uuid: str
    package_name: str
    content: dict
