#!/usr/bin/env python3
import threading
import time

import schedule  # type: ignore
from logger import logger

log = logger(__name__)


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def scheduler(
    job,
    args: object = {},
    interval: int = 1,
    cadence: str = "day",
    run_on_start: bool = False,
):
    """Interval defaults to 1, any integer greater than 1 is accepted.
    Valid cadence options: second, seconds, minute, minutes, hour, hours,
    day, days, week, weeks, monday, tuesday, wednesday, thursday, friday,
    saturday, sunday
    """
    log.info(f"Starting scheduler (runs every {interval} {cadence})...")

    if run_on_start:
        log.info("Running job(s) on scheduler start")
        job(**args)

    getattr(schedule.every(interval), cadence).do(job, **args)

    log.info(f"Next update scheduled in {interval} {cadence}")

    schedule_runner = run_continuously()
    schedule_runner.end = schedule_runner.set

    return schedule_runner
