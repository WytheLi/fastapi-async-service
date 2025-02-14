#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Column, TIMESTAMP, Integer, func, text

from db import Base
from settings import settings


class BaseModel(Base):
    __abstract__ = True

    # created_by = Column(Integer, comment='创建人')
    # updated_by = Column(Integer, comment='更新人')
    created_at = Column(TIMESTAMP(timezone=settings.USE_TZ), nullable=False, default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP(timezone=settings.USE_TZ), nullable=False, default=func.now(), onupdate=func.now(), comment='更新时间')
