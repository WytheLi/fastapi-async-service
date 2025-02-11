from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from loguru import logger


class APSchedulerManager:
    """ 定时任务管理类 """
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_listener(self.job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def job_listener(self, event):
        """监听任务执行的回调函数，记录任务执行结果"""
        if event.exception:
            logger.error(f"Job {event.job_id} failed: {event.exception}")
        # else:
        #     logger.info(f"Job {event.job_id} succeeded")

    def add_job(self, job_func, trigger, **kwargs):
        """添加定时任务"""
        self.scheduler.add_job(job_func, trigger, **kwargs)

    def start(self):
        """启动定时任务调度器"""
        self.scheduler.start()
        logger.info("APScheduler started.")

    def shutdown(self):
        """关闭定时任务调度器"""
        self.scheduler.shutdown()
        logger.info("APScheduler stopped.")


scheduler_manager = APSchedulerManager()
