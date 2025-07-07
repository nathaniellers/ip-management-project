import httpx
import asyncio
import logging
from app.config import Settings
from app.queue.audit_queue import audit_queue

settings = Settings()
logger = logging.getLogger(__name__)

async def audit_worker():
  while True:
    payload = await audit_queue.get()
    max_retries = 3
    base_delay = 0.5

    for attempt in range(max_retries):
      try:
        async with httpx.AsyncClient(timeout=5.0) as client:
          await client.post(
            f"{settings.AUDIT_SERVICE_URL}/api/logs",
            json=payload,
            headers={"x-internal-key": settings.INTERNAL_KEY}
          )
        break
      except Exception as e:
        logger.warning(f"[Audit Retry {attempt + 1}] Failed: {e}")
        await asyncio.sleep(base_delay * (2 ** attempt)) 
    else:
      logger.error(f"Audit log permanently failed: {payload}")

    audit_queue.task_done()
