from celery import shared_task
import time


@shared_task(name="test_connection_task")
def test_connection_task():
    """
    Simple task to test Celery connection
    """
    return {
        "status": "success",
        "message": "Celery connection is working properly!"
    }


@shared_task(name="long_running_task")
def long_running_task(duration=10):
    """
    Task that simulates a long-running process by sleeping for the specified duration

    Args:
        duration (int): Sleep duration in seconds (default: 10)
    """
    # Sleep for the specified duration to simulate a time-consuming task
    time.sleep(duration)

    return {
        "status": "success",
        "message": f"Long running task completed after {duration} seconds!"
    }
