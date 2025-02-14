from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Date, Numeric, Text, Boolean, func

from .abstract import BaseModel


class Country(BaseModel):
    """国家表"""
    __tablename__ = "app_base_country"

    id = Column(Integer, primary_key=True, index=True, comment='自增ID')
    country_name = Column(String(255), unique=True, index=True, comment='国家名称')
    country_name_cn = Column(String(255), comment='国家中文名称')
    symbol = Column(String(10), nullable=True)  # 货币符号 (如 $, €)
    exchange_rate = Column(Numeric(12, 4), nullable=True)  # 对应的汇率，假设是对某基准货币的汇率
    iso_alpha_2 = Column(String(2), unique=True, index=True, comment='ISO 3166-1 alpha-2 国家代码，国际标准')
    iso_alpha_3 = Column(String(3), unique=True, index=True, comment='ISO 3166-1 alpha-3 国家代码，国际标准')


# class Language(BaseModel):
#     """语言表"""
#     __tablename__ = "app_base_language"
#
#     id = Column(Integer, primary_key=True, index=True, comment='自增ID')
#     language_name = Column(String(255), index=True, comment='语言名称')
#     language_name_cn = Column(String(255), comment='语言中文名称')
#     iso_639_1 = Column(String(2), index=True, comment='ISO 639-1 语言代码')
#     iso_639_3 = Column(String(3), index=True, comment='ISO 639-3 语言代码')
#     ietf_bcp47_tag = Column(String(20), index=True, comment='IETF BCP 47 语言代码')
#
#
# class TimeZone(BaseModel):
#     """时区表"""
#     __tablename__ = "app_base_timezone"
#
#     id = Column(Integer, primary_key=True, index=True, comment='自增ID')
#     timezone_code = Column(String(8), unique=True, index=True, comment='时区代码缩写，格式如 CST')
#     timezone_offset = Column(String(16), comment='时区偏移量，格式如UTC+08:00')
#     timezone_country = Column(String(50), comment='时区所属国家')
#     timezone_name = Column(String(50), comment='时区名称')
#     timezone_name_cn = Column(String(50), comment='时区中文名称')
#
#
# class VersionConfig(BaseModel):
#     """版本配置表"""
#     __tablename__ = 'app_base_version'
#
#     id = Column(Integer, primary_key=True, index=True)
#     version_start = Column(String, index=True, comment='版本开始')
#     version_end = Column(String, index=True, comment='版本结束')
#     package_name = Column(String(64), nullable=False, index=True, comment="App包名")
#     language = Column(String, index=True, comment='语言')
#     country = Column(String, index=True, comment='国家')
#     is_mandatory = Column(Integer, default=1, comment='是否强制升级')  # 1 强制升级 0 不是强制升级
#     update_url = Column(String, comment='站外跳转URL地址')
#     is_active = Column(Integer, default=1, comment='是否启用')  # 1 启用 0 未启用
#     remark = Column(String, comment='备注')
#
#     translations = relationship(
#         "Translation",
#         primaryjoin="and_(Translation.table_name=='version_configs', Translation.record_id==foreign(VersionConfig.id))",
#         viewonly=True,
#         uselist=True
#     )
#
#
# class Announcement(BaseModel):
#     """公告配置表"""
#     __tablename__ = 'app_base_announcement'
#
#     id = Column(Integer, primary_key=True, index=True)
#     announcement_icon = Column(String(255), comment='公告底图')
#     package_name = Column(String(64), nullable=False, index=True, comment="App包名")
#     language = Column(String, index=True, comment='语言')
#     country = Column(String, index=True, comment='国家')
#     is_active = Column(Integer, default=1, comment='是否启用')  # 1 启用 0 未启用
#     apply_version = Column(String(128), nullable=False, comment='适用版本号区间（A≤XXX＜B）')
#     remark = Column(String, comment='备注')
#     announcement_type = Column(Integer, default=0, comment='公告类型,0:内容;1:跳转')
#     announcement_weight = Column(Integer, default=1, comment='公告权重')  # 控制公告显示颜色 1：蓝色；2：紫色；3：红色
#     on_shelf_date = Column(TIMESTAMP, default=func.now(), comment='上架日期')
#     down_shelf_date = Column(TIMESTAMP, default=func.now(), comment='下架日期')
#
#     translations = relationship(
#         "Translation",
#         primaryjoin="and_(Translation.table_name=='announcement', Translation.record_id==foreign(Announcement.id))",
#         viewonly=True,
#         uselist=True
#     )
#
#
# class Translation(BaseModel):
#     """多语言配置表"""
#     __tablename__ = 'app_base_translations'
#
#     id = Column(Integer, primary_key=True, index=True)
#     table_name = Column(String, index=True, comment='表名')  # 表名
#     record_id = Column(Integer, index=True, comment='记录ID')  # 记录ID
#     language = Column(String, index=True, comment='语言')  # 语言
#     field_name = Column(String, index=True, comment='字段名')  # 字段名
#     value = Column(String, comment='翻译值')  # 翻译值
#     value_text = Column(Text, comment='文本翻译值')  # 用来存储富文本
