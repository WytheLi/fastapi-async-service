from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class LocaleTimeSchema(BaseModel):
    locale_time: Optional[datetime] = Field(..., description="本机时间")
    china_time: Optional[datetime] = Field(..., description="北京时间")
