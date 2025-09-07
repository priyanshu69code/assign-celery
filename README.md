# Celery Email Project

A Django project with Celery integration for asynchronous task processing, using Redis as the message broker and Django Celery Results for task monitoring.

## Project Structure

- `config/`: Django project settings
- `tasks/`: App for general-purpose Celery tasks
- `email_sender/`: App for email-related Celery tasks
- `docker-compose.yml`: Docker configuration for Redis

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Redis using Docker

```bash
docker-compose up -d
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start Celery Worker

```bash
# In a separate terminal
celery -A config worker -l INFO
```

### 5. Start Celery Beat (Optional, for scheduled tasks)

```bash
# In another separate terminal
celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### 6. Run Django Server

```bash
python manage.py runserver
```

### 7. Test Tasks

```bash
python test_tasks.py
```

## Available Tasks

1. `test_connection_task`: Simple task to verify Celery connection
2. `long_running_task(duration)`: Task with sleep to test async execution
3. `send_test_email(recipient_email)`: Task to simulate sending an email

## Monitoring

- Visit Django admin at `http://localhost:8000/admin/` to view task results
- Use `django_celery_results` and `django_celery_beat` admin interfaces

## Notes

- Redis is configured to run on port 6379
- Timezone is set to 'Asia/Kolkata'
- Result backend is configured to use Django database
