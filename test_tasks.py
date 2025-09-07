#!/usr/bin/env python
"""
Test script to verify Celery task execution
Run this script after starting Redis and Celery worker
"""
import os
import django
import time
import sys
from celery.result import AsyncResult

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Helper function to check task status and result
def check_task_status(task_id=None):
    """
    Check and display the status and result of a task

    Args:
        task_id: ID of the task to check (if None, prompts for input)
    """
    if task_id is None:
        task_id = input("Enter the task ID to check: ")

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

# Import tasks after Django is set up
from tasks.tasks import test_connection_task, long_running_task
from email_sender.tasks import send_test_email

# Run test connection task
print("Running test_connection_task...")
result1 = test_connection_task.delay()
print(f"Task ID: {result1.id}")
print("Waiting for result...")
time.sleep(2)
print(f"Result: {result1.get(timeout=5)}")
print()

# Run long running task with a short duration for testing
print("Running long_running_task with 5 second duration...")
result2 = long_running_task.delay(5)
print(f"Task ID: {result2.id}")
print("Task is running in the background...")
print()

# Run email sending task
print("Running send_test_email task...")
result3 = send_test_email.delay("test@example.com")
print(f"Task ID: {result3.id}")
print("Task is running in the background...")
print()

# Wait for and display results of both tasks
print("Waiting for long_running_task to complete...")
try:
    result2_output = result2.get(timeout=10)  # Wait up to 10 seconds for completion
    print(f"Long running task result: {result2_output}")
except Exception as e:
    print(f"Error waiting for long_running_task: {e}")
print()

print("Waiting for send_test_email task to complete...")
try:
    result3_output = result3.get(timeout=5)  # Wait up to 5 seconds for completion
    print(f"Email task result: {result3_output}")
except Exception as e:
    print(f"Error waiting for send_test_email task: {e}")
print()

# Interactive task status checker
print("=" * 50)
print("Task Status Checker")
print("=" * 50)
print("You can check the status of any task using its ID")
print("Task IDs from this run:")
print(f"1. Test Connection Task: {result1.id}")
print(f"2. Long Running Task: {result2.id}")
print(f"3. Email Sending Task: {result3.id}")
print()

# Allow checking status of specific task
if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
    while True:
        print("\nOptions:")
        print("1. Check test connection task")
        print("2. Check long running task")
        print("3. Check email sending task")
        print("4. Check custom task ID")
        print("q. Quit")

        choice = input("Enter choice: ")

        if choice == '1':
            check_task_status(result1.id)
        elif choice == '2':
            check_task_status(result2.id)
        elif choice == '3':
            check_task_status(result3.id)
        elif choice == '4':
            check_task_status()
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice")
else:
    print("Run with '--interactive' flag to check task statuses interactively")
    print("Example: python test_tasks.py --interactive")
