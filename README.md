# Django Celery Email Integration Project

A Django project with Celery integration for sending emails asynchronously via Gmail SMTP. This project includes a complete email sending infrastructure with Redis as the message broker, HTML email templates, and a dashboard for sending and monitoring emails.

## Project Structure

- `config/`: Django project settings
- `tasks/`: App for general-purpose Celery tasks
- `email_sender/`: App for email-related Celery tasks and APIs
- `templates/`: HTML templates for emails and web interface
- `docker-compose.yml`: Docker configuration for Redis

## Features

- **Asynchronous Email Sending**: Send emails in the background using Celery
- **Multiple Email Types**:
  - Simple text and HTML emails
  - Bulk emails to multiple recipients
  - Template-based emails with dynamic content
  - Emails with attachments
- **API Endpoints**: RESTful API for email operations
- **Status Monitoring**: Track email sending tasks
- **Web Dashboard**: User-friendly interface for sending emails and checking status

## Setup Instructions

### 1. Configure Environment Variables

Copy `.env.example` to `.env` and update with your Gmail credentials:

```bash
cp .env.example .env
# Edit .env with your email credentials
```

**Note**: For Gmail, you need to create an App Password:
1. Go to your Google Account > Security
2. Under "Signing in to Google" select "App passwords"
3. Select "Mail" as the app and your device
4. Click "Generate" and use the 16-character password

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Redis using Docker

```bash
docker-compose up -d
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Start Celery Worker

```bash
# In a separate terminal
celery -A config worker -l INFO
```

### 6. Run Django Server

```bash
python manage.py runserver
```

## Using the Email System

### Web Dashboard

Visit [http://localhost:8000/](http://localhost:8000/) to access the email dashboard where you can:
- Send simple emails
- Send bulk emails to multiple recipients
- Send template-based emails
- Check email task status

### API Endpoints

- `POST /api/send-email/`: Send a simple email
- `POST /api/send-bulk-email/`: Send emails to multiple recipients
- `POST /api/send-template-email/`: Send an email using HTML templates
- `POST /api/send-email-with-attachment/`: Send an email with attachment
- `GET /api/email-status/<task_id>/`: Check status of an email task

### API Example (using curl)

```bash
# Send a simple email
curl -X POST http://localhost:8000/api/send-email/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{"recipient_email": "recipient@example.com", "subject": "Test Email", "message": "Hello from Django Celery!"}'
```

## Original Celery Tasks

1. `test_connection_task`: Simple task to verify Celery connection
2. `long_running_task(duration)`: Task with sleep to test async execution

## Email Tasks

1. `send_email_task(recipient_email, subject, message, html_message)`: Send single email
2. `send_bulk_email_task(recipient_list, subject, message, html_message)`: Send to multiple recipients
3. `send_template_email_task(recipient_email, subject, template_name, context)`: Send using template
4. `send_email_with_attachment_task(recipient_email, subject, message, attachment_path, filename, html_message)`: Send with attachment

## Monitoring

- Visit Django admin at `http://localhost:8000/admin/` to view task results
- Use `django_celery_results` admin interface to see task execution details
- Use the Status Check tab in the web dashboard

## Email Templates

The project includes two sample email templates:
- Welcome email (`templates/email/welcome.html`)
- Notification email (`templates/email/notification.html`)

## Notes

- Redis is configured to run on port 6379
- Timezone is set to 'Asia/Kolkata'
- Result backend is configured to use Django database
