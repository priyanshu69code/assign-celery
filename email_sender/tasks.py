import logging
from celery import shared_task
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import os

# Configure logger
logger = logging.getLogger(__name__)

@shared_task(name="send_email_task")
def send_email_task(recipient_email, subject, message, html_message=None):
    """
    Task to send an email to a single recipient

    Args:
        recipient_email (str): Email address of the recipient
        subject (str): Email subject
        message (str): Plain text message
        html_message (str, optional): HTML content for the email
    """
    try:
        if html_message:
            # Send HTML email
            email_sent = send_mail(
                subject=subject,
                message=message,  # Plain text version
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
        else:
            # Send plain text email
            email_sent = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
            )

        if email_sent:
            logger.info(f"Email sent successfully to {recipient_email}")
            return {
                "status": "success",
                "message": f"Email sent to {recipient_email}",
                "details": {
                    "to": recipient_email,
                    "subject": subject,
                }
            }
        else:
            logger.error(f"Failed to send email to {recipient_email}")
            return {
                "status": "failed",
                "message": f"Failed to send email to {recipient_email}",
            }

    except Exception as e:
        logger.error(f"Error sending email to {recipient_email}: {str(e)}")
        return {
            "status": "error",
            "message": f"Error sending email: {str(e)}",
            "details": {
                "to": recipient_email,
                "subject": subject,
            }
        }


@shared_task(name="send_bulk_email_task")
def send_bulk_email_task(recipient_list, subject, message, html_message=None):
    """
    Task to send emails to multiple recipients

    Args:
        recipient_list (list): List of email addresses
        subject (str): Email subject
        message (str): Plain text message
        html_message (str, optional): HTML content for the email
    """
    results = []
    success_count = 0
    failure_count = 0

    for recipient in recipient_list:
        try:
            # We use the single email task for each recipient
            result = send_email_task(recipient, subject, message, html_message)

            if result["status"] == "success":
                success_count += 1
            else:
                failure_count += 1

            results.append(result)
        except Exception as e:
            logger.error(f"Error in bulk email sending to {recipient}: {str(e)}")
            failure_count += 1
            results.append({
                "status": "error",
                "message": f"Error sending email: {str(e)}",
                "recipient": recipient
            })

    return {
        "status": "completed",
        "summary": {
            "total": len(recipient_list),
            "success": success_count,
            "failed": failure_count,
        },
        "results": results
    }


@shared_task(name="send_template_email_task")
def send_template_email_task(recipient_email, subject, template_name, context=None):
    """
    Task to send an email using a template

    Args:
        recipient_email (str): Email address of the recipient
        subject (str): Email subject
        template_name (str): Name of the template to use
        context (dict, optional): Context data for the template
    """
    if context is None:
        context = {}

    try:
        # Render the HTML content
        html_message = render_to_string(template_name, context)
        # Create plain text version from HTML
        plain_message = strip_tags(html_message)

        return send_email_task(recipient_email, subject, plain_message, html_message)

    except Exception as e:
        logger.error(f"Error sending template email to {recipient_email}: {str(e)}")
        return {
            "status": "error",
            "message": f"Error sending template email: {str(e)}",
            "details": {
                "to": recipient_email,
                "subject": subject,
                "template": template_name,
            }
        }


@shared_task(name="send_email_with_attachment_task")
def send_email_with_attachment_task(recipient_email, subject, message, attachment_path, filename=None, html_message=None):
    """
    Task to send an email with an attachment

    Args:
        recipient_email (str): Email address of the recipient
        subject (str): Email subject
        message (str): Plain text message
        attachment_path (str): Path to the attachment file
        filename (str, optional): Custom filename for the attachment
        html_message (str, optional): HTML content for the email
    """
    try:
        if not os.path.exists(attachment_path):
            return {
                "status": "error",
                "message": f"Attachment file not found: {attachment_path}",
            }

        if not filename:
            filename = os.path.basename(attachment_path)

        # Create email message
        if html_message:
            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
            )
            email.attach_alternative(html_message, "text/html")
        else:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
            )

        # Attach file
        with open(attachment_path, 'rb') as attachment:
            email.attach(filename, attachment.read())

        # Send email
        email_sent = email.send()

        if email_sent:
            logger.info(f"Email with attachment sent successfully to {recipient_email}")
            return {
                "status": "success",
                "message": f"Email with attachment sent to {recipient_email}",
                "details": {
                    "to": recipient_email,
                    "subject": subject,
                    "attachment": filename,
                }
            }
        else:
            logger.error(f"Failed to send email with attachment to {recipient_email}")
            return {
                "status": "failed",
                "message": f"Failed to send email with attachment",
            }

    except Exception as e:
        logger.error(f"Error sending email with attachment to {recipient_email}: {str(e)}")
        return {
            "status": "error",
            "message": f"Error sending email with attachment: {str(e)}",
            "details": {
                "to": recipient_email,
                "subject": subject,
                "attachment": filename or attachment_path,
            }
        }
