import asyncio
import logging
from datetime import datetime
from backend.agents.orchestrator import orchestrator
from backend.agents.follow_up import follow_up_agent

logger = logging.getLogger("ai7.scheduler")

class AutonomousScheduler:
    """
    Autonomous Scheduler (Section 23):
    Runs the continuous agent loop in the background.
    Configurable timing, event-driven triggers, and non-blocking tasks.
    """
    def __init__(self, interval_seconds: int = 3600):
        self.interval_seconds = interval_seconds
        self.is_running = False
        self._task = None

    async def start(self):
        if self.is_running:
            return
        self.is_running = True
        logger.info("Autonomous Career Agent background loop started.")
        self._task = asyncio.create_task(self._loop())

    async def stop(self):
        self.is_running = False
        if self._task:
            self._task.cancel()
        logger.info("Autonomous Career Agent background loop stopped.")

    async def _loop(self):
        while self.is_running:
            try:
                logger.info("Scheduler triggering autonomous pipeline cycle...")
                orchestrator.run_full_pipeline_cycle()
                follow_up_agent.process_scheduled_follow_ups()
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")

            await asyncio.sleep(self.interval_seconds)

scheduler = AutonomousScheduler()
