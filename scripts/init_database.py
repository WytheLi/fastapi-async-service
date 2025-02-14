import asyncio

from dotenv import load_dotenv
load_dotenv()


from db.async_engine import async_session
from models import Role


async def init_database(session):
    """
    初始化数据库
    :param session:
    :return:
    """
    admin_role = Role(role_name='管理员', role_code='admin')
    internal_user_role = Role(role_name='内部用户', role_code='internal')
    normal_user_role = Role(role_name='普通用户', role_code='normal')
    session.add_all([admin_role, internal_user_role, normal_user_role])
    await session.commit()


async def main():
    async with async_session() as session:
        await init_database(session)


if __name__ == '__main__':
    asyncio.run(main())
