#!/usr/bin/env python
"""
Task status checker script
This script allows you to check the status and result of any Celery task by its ID
"""
import os
import django
import sys
from celery.result import AsyncResult

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def check_task(task_id):
    """Check and print the status and result of a task"""
    task_result = AsyncResult(task_id)

    print(f"\nTask ID: {task_id}")
    print(f"Status: {task_result.status}")

    if task_result.ready():
        if task_result.successful():
            print(f"Result: {task_result.get()}")
        else:
            print(f"Task failed: {task_result.result}")
            print(f"Traceback: {task_result.traceback}")
    else:
        print("Task is still running...")

    return task_result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
        check_task(task_id)
    else:
        task_id = input("Enter the task ID to check: ")
        check_task(task_id)
