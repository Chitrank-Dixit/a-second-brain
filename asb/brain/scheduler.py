# asb/brain/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from asb.brain.reflection import ReflectionEngine
import time
from asb.brain.logger import setup_logger
from asb.brain.memory_compressor import MemoryCompressor
from asb.brain.research_agent import ResearchAgent
log = setup_logger()


def start_daily_reflection(timeout_hours: int = 1):
    """
    Start a background reflection job that runs daily,
    but automatically stops after `timeout_hours`.
    """
    engine = ReflectionEngine()
    scheduler = BackgroundScheduler()
    scheduler.add_job(engine.reflect, 'interval', hours=24)
    scheduler.start()

    log.info(f"🕰️ Daily reflection job started. Will run for {timeout_hours} hour(s).")
    start_time = time.time()
    timeout = timeout_hours * 3600

    try:
        while True:
            time.sleep(30)
            if time.time() - start_time >= timeout:
                log.info("⏱️ Timeout reached — stopping scheduler.")
                scheduler.shutdown()
                break
    except KeyboardInterrupt:
        log.info("🧩 Manual interrupt — shutting down.")
        scheduler.shutdown()

def start_weekly_compression():
    compressor = MemoryCompressor()
    scheduler = BackgroundScheduler()
    scheduler.add_job(compressor.compress_old_reflections, "interval", days=7)
    scheduler.start()

def start_weekly_research():
    ra = ResearchAgent()
    scheduler = BackgroundScheduler()
    scheduler.add_job(ra.run_autonomous_research, 'interval', days=7)
    scheduler.start()
    print("🤖 Weekly autonomous research enabled.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()