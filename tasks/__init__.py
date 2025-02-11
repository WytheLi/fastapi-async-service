from typing import Any

from core.scheduler import APSchedulerManager


def scheduler_add_job(scheduler_manager: APSchedulerManager):
    """
    配置定时任务
    """
    # scheduler_manager.add_job(Any, trigger='cron', hour=0, minute=0, second=1)  # 00:00:01执行
    pass
