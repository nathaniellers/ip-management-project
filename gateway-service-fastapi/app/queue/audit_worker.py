import httpx
import logging
from app.config import Settings
from app.queue.audit_queue import audit_queue

settings = Settings()
logger = logging.getLogger(__name__)

async def audit_worker():
  while True:
    payload = await audit_queue.get()
    try:
      async with httpx.AsyncClient(timeout=5.0) as client:
        await client.post(
          f"{settings.AUDIT_SERVICE_URL}/api/audit",
          json=payload,
          headers={"x-internal-key": settings.INTERNAL_KEY}
        )
    except Exception as e:
      logger.error("Audit worker failed to send log: %s", e)
    finally:
      audit_queue.task_done()
