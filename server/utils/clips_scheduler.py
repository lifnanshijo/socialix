"""
Clips Scheduler - Automated task runner for expired clips cleanup
Handles periodic deletion of expired clips using APScheduler
"""

from apscheduler.schedulers.background import BackgroundScheduler
from models.clip import Clip
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ClipsScheduler:
    """Scheduler for background tasks related to clips"""

    scheduler = None

    @staticmethod
    def init_scheduler(app):
        """
        Initialize the background scheduler
        
        Args:
            app: Flask app instance
        """
        ClipsScheduler.scheduler = BackgroundScheduler()

        # Schedule cleanup task to run every hour
        ClipsScheduler.scheduler.add_job(
            func=ClipsScheduler.cleanup_expired_clips,
            trigger="interval",
            hours=1,
            id='cleanup_expired_clips',
            name='Delete expired clips',
            replace_existing=True
        )

        # Optional: Schedule cleanup every 30 minutes for more frequent cleanup
        # ClipsScheduler.scheduler.add_job(
        #     func=ClipsScheduler.cleanup_expired_clips,
        #     trigger="interval",
        #     minutes=30,
        #     id='cleanup_expired_clips_frequent',
        #     name='Delete expired clips (frequent)',
        #     replace_existing=True
        # )

        # Start scheduler in background
        if not ClipsScheduler.scheduler.running:
            ClipsScheduler.scheduler.start()
            logger.info("Clips scheduler initialized and started")

    @staticmethod
    def cleanup_expired_clips():
        """
        Background task to delete expired clips
        This is called automatically by the scheduler
        """
        try:
            logger.info(f"Starting expired clips cleanup at {datetime.now()}")
            deleted_count = Clip.delete_expired_clips()
            logger.info(f"Cleanup completed. Deleted {deleted_count} expired clips")
        except Exception as e:
            logger.error(f"Error during clips cleanup: {str(e)}")

    @staticmethod
    def shutdown_scheduler():
        """
        Shutdown the scheduler gracefully
        """
        if ClipsScheduler.scheduler and ClipsScheduler.scheduler.running:
            ClipsScheduler.scheduler.shutdown()
            logger.info("Clips scheduler shut down")


# Alternative: Using schedule library (simpler but less powerful)
import schedule
import threading

class SimpleClipsScheduler:
    """Simple scheduler using schedule library"""

    @staticmethod
    def start_scheduler():
        """
        Start simple scheduler in a background thread
        """
        # Schedule cleanup every hour
        schedule.every().hour.do(Clip.delete_expired_clips)

        # Run scheduler in background thread
        def run_scheduler():
            while True:
                schedule.run_pending()
                import time
                time.sleep(60)  # Check every minute

        thread = threading.Thread(target=run_scheduler, daemon=True)
        thread.start()
        logger.info("Simple scheduler started in background thread")


# Alternative: Using Celery for distributed task queue (production-grade)
# This would require Redis and Celery setup
"""
from celery import Celery, Task
from celery.schedules import crontab

# Initialize Celery
celery = Celery(__name__)
celery.conf.broker_url = 'redis://localhost:6379'
celery.conf.result_backend = 'redis://localhost:6379'

@celery.task
def cleanup_expired_clips_task():
    '''Celery task to cleanup expired clips'''
    return Clip.delete_expired_clips()

# Schedule the task
celery.conf.beat_schedule = {
    'cleanup-expired-clips': {
        'task': 'tasks.cleanup_expired_clips_task',
        'schedule': crontab(minute=0),  # Run every hour
    },
}
"""
