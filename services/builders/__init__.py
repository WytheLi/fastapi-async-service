from typing import Callable

from loguru import logger


class BuilderFactory(object):
    """注册器类"""
    # 事件处理器注册字典
    event_handlers = {}

    @classmethod
    def register(cls, event_type: str) -> Callable:
        """
        将事件处理器类注册到注册器字典中，形如：@builders.BuilderFactory.register(EventType.USER_ACTIVITY.value)
        @param event_type: 实践类型
        """
        def inner_wrapper(wrapped_class):
            if event_type in cls.event_handlers:
                logger.warning(f"Builder [{event_type}] already exists. Will replace it")
            cls.event_handlers[event_type] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def get_handler_cls(cls, event_type: str):
        if event_type not in cls.event_handlers:
            logger.warning(f"Event Type: [{event_type}] does not exist in the registry")
            raise NotImplementedError

        return cls.event_handlers[event_type]


class BaseEventHandler:
    """所有事件处理器的基类，提供统一接口"""
    async def handle(self, data: dict):
        raise NotImplementedError("Handle method must be implemented in subclasses")


from .user_activity import UserActivityEventHandler
