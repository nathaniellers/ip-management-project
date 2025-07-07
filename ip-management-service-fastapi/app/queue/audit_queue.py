import asyncio
from typing import Dict

audit_queue = asyncio.Queue()

async def enqueue_audit_log(payload: Dict):
  await audit_queue.put(payload)
