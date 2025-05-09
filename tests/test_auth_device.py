from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select

from models import AuthDevice
from models import AuthLogs
from models import Role
from schemas.account import DeviceSchema
from services.account import UserResource
from utils.crypt import verity_password
from utils.geoip import GeoIPService
from utils.status_info import StatusInfo


@pytest.fixture
def mocked_device_data():
    """模拟设备数据"""
    return DeviceSchema(device_id="test_device_123", package_name="com.test.app")


@pytest_asyncio.fixture
async def mocked_data():
    return DeviceSchema(
        device_id="test_device_456",
        package_name="com.test.app",
        country="Philippines",
        ip_address="127.0.0.1",
        user_agent="Test-Agent",
        isp="TestISP",
    )


@pytest_asyncio.fixture
async def mocked_role(async_session):
    """模拟设备数据"""
    role = Role(role_name="普通用户", role_code="normal")
    async_session.add(role)
    await async_session.commit()
    return role


@pytest.mark.asyncio
class TestAuthDevice:
    """设备注册接口测试套件"""

    REQUEST_HEADERS = {"X-Forwarded-For": "127.0.0.1", "User-Agent": "TestAgent"}

    @patch.object(GeoIPService, "get_country")
    @patch("services.repo.account.query_auth_device")
    @patch.object(UserResource, "create_user", new_callable=AsyncMock)
    @patch("utils.signature.create_access_token")
    async def test_new_device_registration(
        self,
        mocked_token,
        mocked_user,
        mocked_auth_device,
        mocked_country,
        client: AsyncClient,
        async_session,
        mocked_device_data,
    ):
        """测试新设备首次注册成功"""
        mocked_country.return_value = {"country": "US", "isp": "TestISP"}
        mocked_auth_device.return_value = None  # 设备未注册
        mocked_user.return_value = AsyncMock(id=1)
        mocked_token.return_value = "mock_token"

        # 执行请求
        response = await client.post(
            "/api/v1/auth/device", json=mocked_device_data.model_dump(), headers=self.REQUEST_HEADERS
        )

        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == StatusInfo.Success["code"]
        assert data["data"]["token"] == "mock_token"

    async def test_existing_device_login(self, client: AsyncClient, async_session):
        """测试已注册设备重复请求"""
        pass

    async def test_disabled_user_login(self, client: AsyncClient, async_session):
        """测试禁用用户登录"""
        pass

    async def test_create_user(self, async_session, mocked_role, mocked_data):
        user = await UserResource.create_user(async_session, mocked_data)
        await async_session.commit()

        # 断言返回的用户对象
        assert user is not None
        assert user.id is not None
        assert verity_password(mocked_data.device_id, user.password_digest)

        # 验证用户与角色的关联：用户角色列表中应包含刚插入的 role
        assert mocked_role in user.roles

        # 验证设备认证记录是否已插入
        auth_device_query = await async_session.execute(
            select(AuthDevice).where(AuthDevice.user_uuid == user.user_uuid)
        )
        auth_device = auth_device_query.scalars().first()
        assert auth_device is not None
        assert auth_device.device_id == mocked_data.device_id
        assert auth_device.package_name == mocked_data.package_name

        # 验证登录日志记录是否已插入
        login_log_query = await async_session.execute(select(AuthLogs).where(AuthLogs.user_uuid == user.user_uuid))
        login_log = login_log_query.scalars().first()
        assert login_log is not None
        assert login_log.device_id == mocked_data.device_id
        assert login_log.user_agent == mocked_data.user_agent
