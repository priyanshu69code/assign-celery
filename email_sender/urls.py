from django.urls import path
from . import views

app_name = 'email_sender'

urlpatterns = [
    # Email sending endpoints
    path('send-email/', views.SendEmailView.as_view(), name='send_email'),
    path('send-bulk-email/', views.SendBulkEmailView.as_view(), name='send_bulk_email'),
    path('send-template-email/', views.SendTemplateEmailView.as_view(), name='send_template_email'),
    path('send-email-with-attachment/', views.SendEmailWithAttachmentView.as_view(), name='send_email_with_attachment'),

    # Email status endpoint
    path('email-status/<str:task_id>/', views.EmailTaskStatusView.as_view(), name='email_status'),
]
