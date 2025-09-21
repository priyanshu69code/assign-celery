#!/usr/bin/env python
"""
Demonstration script to show how to use the email sending tasks programmatically.
Run this script to test various email sending features.

Usage:
    python demo_emails.py [recipient_email]

If recipient_email is not provided, it will use test@example.com as the default.
"""
import os
import sys
import django
import time
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Import tasks after Django is set up
from email_sender.tasks import (
    send_email_task,
    send_bulk_email_task,
    send_template_email_task,
    send_email_with_attachment_task
)


def print_separator(title):
    """Print a separator with a title"""
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def run_task_and_check_result(task_result, task_name):
    """Run a task and check its result"""
    print(f"Task ID: {task_result.id}")
    print(f"Task Status: {task_result.status}")
    print("Waiting for task to complete...")

    try:
        # Wait for the task to complete with a timeout
        result = task_result.get(timeout=10)
        print(f"Task Completed. Result:")
        print(json.dumps(result, indent=4))

    except Exception as e:
        print(f"Error waiting for task result: {e}")


def main():
    # Check if recipient email was provided as command line argument
    if len(sys.argv) > 1:
        recipient_email = sys.argv[1]
    else:
        recipient_email = "test@example.com"

    print(f"Using recipient email: {recipient_email}")

    # 1. Simple Email
    print_separator("1. Sending Simple Email")
    task1 = send_email_task.delay(
        recipient_email=recipient_email,
        subject="Test Simple Email",
        message="This is a test email sent using Celery task."
    )
    run_task_and_check_result(task1, "send_email_task")

    # 2. HTML Email
    print_separator("2. Sending HTML Email")
    html_content = """
    <div style="background-color: #f0f0f0; padding: 20px; font-family: Arial, sans-serif;">
        <h2 style="color: #0066cc;">Test HTML Email</h2>
        <p>This is a <strong>formatted</strong> email with <span style="color: green;">HTML</span> content.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
            <li>Item 3</li>
        </ul>
        <p>Sent using Celery tasks.</p>
    </div>
    """
    task2 = send_email_task.delay(
        recipient_email=recipient_email,
        subject="Test HTML Email",
        message="This is a plain text version of the HTML email.",
        html_message=html_content
    )
    run_task_and_check_result(task2, "send_email_task (HTML)")

    # 3. Bulk Email
    print_separator("3. Sending Bulk Email")
    recipients = [
        recipient_email,
        "user1@example.com",  # These won't be sent if invalid
        "user2@example.com"   # These are just for demonstration
    ]
    task3 = send_bulk_email_task.delay(
        recipient_list=recipients,
        subject="Test Bulk Email",
        message="This is a bulk test email sent to multiple recipients."
    )
    run_task_and_check_result(task3, "send_bulk_email_task")

    # 4. Template Email (Welcome)
    print_separator("4. Sending Welcome Template Email")
    context = {
        "name": "John Doe",
    }
    task4 = send_template_email_task.delay(
        recipient_email=recipient_email,
        subject="Welcome to Our Service",
        template_name="email/welcome.html",
        context=context
    )
    run_task_and_check_result(task4, "send_template_email_task (Welcome)")

    # 5. Template Email (Notification)
    print_separator("5. Sending Notification Template Email")
    context = {
        "name": "John Doe",
        "notification_title": "New Feature Available",
        "notification_message": "We've just launched an amazing new feature. Check it out now!"
    }
    task5 = send_template_email_task.delay(
        recipient_email=recipient_email,
        subject="Important Notification",
        template_name="email/notification.html",
        context=context
    )
    run_task_and_check_result(task5, "send_template_email_task (Notification)")

    # 6. Email with Attachment
    print_separator("6. Sending Email with Attachment")
    attachment_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  "media", "uploads", "sample.txt")
    task6 = send_email_with_attachment_task.delay(
        recipient_email=recipient_email,
        subject="Test Email with Attachment",
        message="This is a test email with an attachment.",
        attachment_path=attachment_path,
        filename="test-attachment.txt"
    )
    run_task_and_check_result(task6, "send_email_with_attachment_task")


if __name__ == "__main__":
    main()
