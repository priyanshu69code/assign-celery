from celery import shared_task


@shared_task(name="send_test_email")
def send_test_email(recipient_email):
    """
    Task to simulate sending a test email

    Args:
        recipient_email (str): Email address of the recipient
    """
    # This is just a simulation - no actual email is sent
    # In a real application, you would use Django's send_mail function

    # Simulate some processing time
    import time
    time.sleep(2)

    return {
        "status": "success",
        "message": f"Test email sent to {recipient_email}",
        "details": {
            "to": recipient_email,
            "subject": "Celery Test Email",
            "body": "This is a test email from Celery."
        }
    }
