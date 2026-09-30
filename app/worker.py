"""
Background worker for Auction Marketplace
Uses APScheduler for scheduled tasks
"""
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Initialize scheduler
scheduler = AsyncIOScheduler()


def scheduled_task():
    """Example scheduled task - will be replaced with actual auction closing logic"""
    print("Worker running scheduled task...")


def start_worker():
    """Start the background worker"""
    print("Starting Auction Marketplace Worker...")
    
    # Add example job - runs every minute
    scheduler.add_job(
        scheduled_task,
        trigger=IntervalTrigger(minutes=1),
        id="example_task",
        name="Example scheduled task",
        replace_existing=True
    )
    
    scheduler.start()
    print("Worker started successfully")
    
    # Keep the worker running
    try:
        import asyncio
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Worker shut down")


if __name__ == "__main__":
    start_worker()
