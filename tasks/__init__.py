from core.scheduler import APSchedulerManager
from tasks.example import job


def scheduler_add_jobs(scheduler_manager: APSchedulerManager):
    """
    配置定时任务
    """
    # scheduler_manager.add_job(Any, trigger='cron', hour=0, minute=0, second=1)  # 00:00:01执行
    pass
