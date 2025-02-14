from typing import Optional

from pydantic import BaseModel, Field


class DeviceSchema(BaseModel):
    device_id: Optional[str]
    package_name: Optional[str]
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    hardware_name: Optional[str] = None
    push_token: Optional[str] = None
    app_name: Optional[str] = None
    app_version: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    ad_id: Optional[str] = None
    ad_id_type: Optional[str] = None
    referrer: Optional[str] = None
    attribution_source: Optional[str] = None
    referrer_account_id: Optional[str] = None
    referrer_adgroup_id: Optional[str] = None
    referrer_adgroup_name: Optional[str] = None
    referrer_campaign_id: Optional[str] = None
    referrer_campaign_group_id: Optional[str] = None
    referrer_campaign_name: Optional[str] = None
    referrer_ad_id: Optional[str] = None
    referrer_ad_name: Optional[str] = None

    class Config:
        extra = 'allow'     # 允许拓展字段


class UserSchema(BaseModel):
    id: Optional[int] = Field(..., description="自增ID")
    user_uuid: Optional[str] = Field(..., description="用户uuid")
    user_code: Optional[str] = Field(..., description="邀请码")
    status: Optional[int] = Field(..., description="账号状态")
    show_name: Optional[str] = Field(..., description="显示用户名")
    avatar: Optional[str] = Field(..., description="头像")
    language: Optional[str] = Field(..., description="使用语言")
    country: Optional[str] = Field(..., description="所属地区")

    class Config:
        from_attributes = True
