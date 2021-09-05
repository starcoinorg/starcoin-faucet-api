from celery.result import AsyncResult
from app.worker import scrape_twitter
from datetime import datetime

async def scrape(id: int,platform: str, url: str, created_at: str):
    # ！！ platform ：facebook
    return scrape_twitter.delay(id, url, datetime.timestamp(created_at))

async def get_result(task_id: str):
    task = AsyncResult(task_id)
    return task.result
