from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from settings import settings


class APSchedulerManager:
    """定时任务管理类"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler(
            jobstores=settings.SCHEDULER_JOBSTORE,
            executors=settings.SCHEDULER_EXECUTOR,
            job_defaults=settings.SCHEDULER_JOB_DEFAULTS,
            timezone=settings.SCHEDULER_TIMEZONE,
        )
        self.scheduler.add_listener(self.job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def job_listener(self, event):
        """监听任务执行的回调函数，记录任务执行结果"""
        if event.exception:
            logger.error(f"Job {event.job_id} failed: {event.exception}")
        # else:
        #     logger.info(f"Job {event.job_id} succeeded")

    def add_job(self, func, trigger, **kwargs):
        """添加定时任务"""
        # job  = self.scheduler.add_job(func, trigger, **kwargs)
        # logger.info(f"AsyncIOScheduler Job added: {job.id} ({func.__name__})")
        self.scheduler.add_job(func, trigger, **kwargs)

    def remove_job(self, job_id):
        """移除任务"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"AsyncIOScheduler Job removed: {job_id}")
        except JobLookupError:
            logger.warning(f"AsyncIOScheduler Job not found: {job_id}")

    def list_jobs(self):
        """列出所有任务"""
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            logger.info(f"AsyncIOScheduler Job: {job.id}, Next Run: {job.next_run_time}")
        return jobs

    def start(self):
        """启动定时任务调度器"""
        if not self.scheduler.running:
            self.scheduler.start()

    def shutdown(self):
        """关闭定时任务调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown()


scheduler_manager = APSchedulerManager()
