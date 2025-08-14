from fastapi import APIRouter
from starlette.requests import Request

from core.scheduler import scheduler_manager

router = APIRouter()


@router.get("", name="scheduler:get_jobs", response_model=list)
async def get_scheduler_jobs(request: Request):
    jobs = scheduler_manager.list_jobs()
    jobs = [{k: v for k, v in job.__getstate__().items() if k != "trigger"} for job in jobs]
    return jobs
