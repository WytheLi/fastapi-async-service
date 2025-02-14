import uuid
from enum import Enum

from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, DateTime, Date, event, text, Boolean, Index, Float

from db import Base
from utils.shortcode_converter import ShortCodeUtils
from .abstract import BaseModel


# 用户角色关联表
app_user_role_rel = Table(
    'app_user_role_rel', Base.metadata,
    Column('user_id', Integer, index=True, comment='用户唯一标识'),
    Column('role_id', Integer, index=True, comment='角色唯一标识')
)


# 角色权限关联表
app_role_perms_rel = Table(
    'app_role_perms_rel', Base.metadata,
    Column('role_id', Integer, index=True, comment='角色唯一标识'),
    Column('perms_id', Integer, index=True, comment='权限唯一标识')
)


class User(BaseModel):
    """用户表"""
    __tablename__ = "app_user"

    class Status(Enum):
        ENABLE = 1  # 正常用户
        DISABLE = 2  # 已禁用
        LOCKED = 3  # 已锁定

    class Gender(Enum):
        UNKNOWN = 0
        MALE = 1
        FEMALE = 2

    class NamePrefix(Enum):
        """ 默认用户名前缀 """
        VISITOR = 'Visitor'

    id = Column(Integer, primary_key=True, index=True, comment='自增ID，在单库单表中唯一')
    user_uuid = Column(String(50), unique=True, index=True, default=lambda: str(uuid.uuid4()), comment='uuid')  # 用户全局唯一标识
    user_code = Column(String(6), unique=True, index=True, comment='邀请码')  # 用户外部唯一标识，6位大写字母+数字组合
    user_name = Column(String(50), comment='用户名')
    display_name = Column(String(50), comment='界面显示名（昵称）')
    password_digest = Column(String(256), nullable=False, comment='登录用户密码的哈希值')
    status = Column(Integer, comment='帐号状态')
    avatar = Column(String(256), comment='头像')
    gender = Column(Integer, comment='性别')
    birthday = Column(Date, comment='生日')
    language = Column(String(8), comment='语言, zh-CN|en-US|en-GB')
    bio = Column(String(500), comment='个人简介')
    email = Column(String(256), index=True, comment='邮箱地址')
    phone = Column(String(16), index=True, comment='手机号')
    country = Column(String(50), comment='国家')
    city = Column(String(50), comment='城市')
    address = Column(String(256), comment='地址')
    remark = Column(String(500), comment='备注')
    last_login = Column(DateTime, comment='最后登录时间')
    is_delete = Column(Boolean, default=False, comment='用户是否被删除')

    roles = relationship(
        'Role',  # 关联表类名
        secondary=app_user_role_rel,  # 指定多对多关联表类名
        primaryjoin='User.id == app_user_role_rel.c.user_id',
        secondaryjoin='Role.id == app_user_role_rel.c.role_id',
        back_populates="users",  # 关联表类中反向引用的名称属性
        lazy='selectin'  # 改成预加载，减少数据库查询次数，直接返回role信息
    )
    # 玩家已解锁关卡
    # screw_pull_player_level_unlock_rel表没有定义外键约束，这里显式的指定联接条件
    # unlock_levels = relationship(
    #     'ScrewPullLevels',
    #     secondary=screw_pull_player_level_unlock_rel,
    #     primaryjoin='User.id == screw_pull_player_level_unlock_rel.c.user_id',
    #     secondaryjoin='ScrewPullLevels.id == screw_pull_player_level_unlock_rel.c.level_id'
    # )

    def setattr_user_code(self, uid):
        shortcode_utils = ShortCodeUtils()
        # 这里如果不分表，暂时取自增id生成唯一code标识是可行的
        self.user_code = shortcode_utils.encode_gen(uid)

    def setattr_username(self):
        self.user_name = self.NamePrefix.VISITOR.value + '-' + self.user_code

    @property
    def show_name(self):
        return self.display_name or self.user_name

    def setattr_avatar(self, package_name: str):
        pass


class Role(BaseModel):
    """角色表"""
    __tablename__ = "app_role"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(16), nullable=False, unique=True, index=True, comment='角色名')
    role_code = Column(String(16), nullable=False, unique=True, index=True, comment='角色标识，不能修改')
    remark = Column(String(256), comment='备注')

    users = relationship(
        'User',
        secondary=app_user_role_rel,
        primaryjoin='Role.id == app_user_role_rel.c.role_id',
        secondaryjoin='User.id == app_user_role_rel.c.user_id',
        back_populates='roles',
        lazy='dynamic'  # 懒加载，提交时才生效，适合数据量大的情况，如：user_query = roles.users、users = await user_query.all()
    )

    perms = relationship(
        'Perms',
        secondary=app_role_perms_rel,
        primaryjoin='Role.id == app_role_perms_rel.c.role_id',
        secondaryjoin='Perms.id == app_role_perms_rel.c.perms_id',
        back_populates="roles",
        lazy='selectin',  # 预加载，适合数据量小，如：await db.execute(select(Role).options(selectinload(Role.perms))
        order_by="Perms.order"
    )


class Perms(BaseModel):
    """权限表"""
    __tablename__ = 'app_perms'

    id = Column(Integer, primary_key=True, index=True, comment='自增ID')
    parent_id = Column(Integer, index=True, default=0, comment='父级ID，上级权限ID')
    current_id = Column(Integer, index=True, comment='当前权限ID')
    perms_title = Column(String(128), comment='权限名')
    perms_type = Column(Integer, comment='权限类型，目录|菜单页|普通页｜按钮')
    perms_icon = Column(String(256), comment='权限图标名')
    perms_comp = Column(String(64), comment='站内前端组件名')
    perms_method = Column(String(8), comment='站内接口方法, get|post|put|delete|patch')
    perms_path = Column(String(64), nullable=False, comment='站内接口路径')
    perms_url = Column(String(255), comment='站外外链请求地址')
    order = Column(Integer, index=True, default=0, comment='排序')

    roles = relationship(
        'Role',
        secondary=app_role_perms_rel,
        primaryjoin='Perms.id == app_role_perms_rel.c.perms_id',
        secondaryjoin='Role.id == app_role_perms_rel.c.role_id',
        back_populates='perms',
        lazy='dynamic'
    )


class AuthSNS(BaseModel):
    """用户社交账号关联表"""
    __tablename__ = "app_auth_sns"

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增ID')
    user_uuid = Column(String(50), nullable=False, index=True, comment='用户唯一标识')
    provider = Column(String(16), index=True, comment='社交平台（google|facebook|twitter|line|instagram|tiktok|github|linkedin|apple|microsoft）')
    openid = Column(String(32), index=True, unique=True, comment='社交平台用户唯一标识')
    email = Column(String(50), index=True, comment='用户邮箱')
    phone = Column(String(16), comment='用户手机号')
    nickname = Column(String(50), comment='用户昵称')
    avatar = Column(String(255), comment='用户头像URL')
    gender = Column(Integer, comment='用户性别（male|female|unknown）')
    locale = Column(String(8), comment='用户语言')
    region = Column(String(50), comment='用户地区')

    __table_args__ = (
        Index('idx_user_provider', 'user_uuid', 'provider', unique=True),
    )


class AuthDevice(BaseModel):
    """设备信息表（在账号注册时，应用安装首次启动时的设备信息）"""
    __tablename__ = "app_auth_device"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(String(50), index=True, comment='用户唯一标识')
    device_id = Column(String(50), comment='设备id，唯一标识指纹')
    package_name = Column(String(32), comment='当前应用包名，应用唯一标识')
    ip_address = Column(String(50), comment='网络IP')
    user_agent = Column(String(255), comment='设备用户代理')
    isp = Column(String(50), comment='网络运营商，云服务ip、机房ip、公司ip、住宅ip等，根据网络IP自动获取')
    device_name = Column(String(50), comment='设备型号名')
    device_type = Column(String(8), comment='设备类型，phone|tablet|pc|other')
    hardware_name = Column(String(32), comment='设备硬件名')
    push_token = Column(String(50), index=True, comment='消息推送token，如：firebase cloud messaging的推送token')
    app_name = Column(String(32), comment='当前应用名（商店名称）')
    app_version = Column(String(4), comment='当前应用版本号')
    os_name = Column(String(8), comment='系统名，android|ios|windows|mac|linux|other')
    os_version = Column(String(8), comment='系统版本')
    country = Column(String(50), comment='系统国家')
    language = Column(String(8), comment='系统语言')
    timezone = Column(String(50), comment='系统时区')
    screen_width = Column(Integer, comment='屏幕宽度')
    screen_height = Column(Integer, comment='屏幕高度')
    screen_density = Column(Float, comment='屏幕像素分辨率')
    external_storage = Column(Float, comment='手机外置存储空间GB')
    external_storage_overage = Column(Float, comment='手机外置存储空间剩余GB')
    network_carrier = Column(String(16), comment='特指设备的电信运营商，如Verizon、AT&T、Sprint、T-Mobile')
    ad_id = Column(String(50), comment='设备广告标识符')
    ad_id_type = Column(String(16), comment='广告标识类型，gaid|idfa|oaid|tifa|vida|rida|fire_adid|other')
    referrer = Column(String(255), comment='谷歌深度链接')
    attribution_source = Column(String(255), comment='归因来源（adjust归因结果/referrer解析utm_source）')
    referrer_account_id = Column(String(255), comment='投放的广告账户id')
    referrer_adgroup_id = Column(String(255), comment='投放的广告组id')
    referrer_adgroup_name = Column(String(255), comment='投放的广告组名')
    referrer_campaign_id = Column(String(255), comment='投放的广告系列名')
    referrer_campaign_group_id = Column(String(255), comment='投放的广告系列归属组id名')
    referrer_campaign_name = Column(String(255), comment='投放的广告系列名')
    referrer_ad_id = Column(String(255), comment='投放的广告ID')
    referrer_ad_name = Column(String(255), comment='投放的广告名（预留）')

    __table_args__ = (
        Index('idx_u_d_p', 'user_uuid', 'device_id', 'package_name', unique=True),  # 创建组合唯一索引
    )


class AuthLogs(BaseModel):
    """ 登录认证日志表 """
    __tablename__ = "app_auth_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(String(50), index=True, comment='用户唯一标识')
    role_code = Column(String(16), comment='角色标识')
    device_id = Column(String(50), comment='设备id，唯一标识指纹')
    device_name = Column(String(50), comment='设备型号名')
    os_name = Column(String(16), comment='系统名，android|ios|windows|mac|linux|other')
    os_version = Column(String(8), comment='系统版本')
    ip_address = Column(String(50), comment='网络IP')
    user_agent = Column(String(255), comment='设备用户代理')
    isp = Column(String(50), comment='网络运营商，机房ip、住宅ip等，根据网络IP库自动获取')
    continent = Column(String(255), comment='所在大洲，根据网络IP库自动获取')
    country = Column(String(50), comment='所在国家，根据网络IP库自动获取')
    province = Column(String(255), comment='所在省份，根据网络IP库自动获取')
    city = Column(String(255), comment='所在城市，根据网络IP库自动获取')
    district = Column(String(255), comment='所在区县，根据网络IP库自动获取')
    area_code = Column(String(255), comment='邮编区号，根据网络IP库自动获取')
    country_code = Column(String(255), comment='国家代码，根据网络IP库自动获取')
    longitude = Column(Float, comment='经度')
    latitude = Column(Float, comment='纬度')
