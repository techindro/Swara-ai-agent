"""Task scheduler using the `schedule` library."""

import asyncio
import schedule
import time
import threading
from loguru import logger


class Scheduler:
    """Wraps the `schedule` library for async task scheduling."""

    def every_day_at(self, time_str: str, coro_func) -> None:
        """Schedule an async coroutine to run every day at a specific time."""
        def run():
            asyncio.run(coro_func())

        schedule.every().day.at(time_str).do(run)
        logger.info(f"⏰ Scheduled daily at {time_str}: {coro_func.__name__}")

    def every_n_minutes(self, n: int, coro_func) -> None:
        """Schedule an async coroutine to run every N minutes."""
        def run():
            asyncio.run(coro_func())

        schedule.every(n).minutes.do(run)
        logger.info(f"⏰ Scheduled every {n}min: {coro_func.__name__}")

    def run_forever(self) -> None:
        """Block and run all pending scheduled jobs."""
        logger.info("🔄 Scheduler running... (Ctrl+C to stop)")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Scheduler stopped.")
