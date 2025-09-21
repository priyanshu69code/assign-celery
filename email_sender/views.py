from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from .tasks import (
    send_email_task,
    send_bulk_email_task,
    send_template_email_task,
    send_email_with_attachment_task,
)
from .serializers import (
    EmailSerializer,
    BulkEmailSerializer,
    TemplateEmailSerializer,
    EmailWithAttachmentSerializer,
)


class SendEmailView(APIView):
    """API view for sending a single email"""

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            task = send_email_task.delay(
                recipient_email=serializer.validated_data['recipient_email'],
                subject=serializer.validated_data['subject'],
                message=serializer.validated_data['message'],
                html_message=serializer.validated_data.get('html_message'),
            )
            return Response({
                'task_id': task.id,
                'status': 'pending',
                'message': 'Email task has been queued'
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendBulkEmailView(APIView):
    """API view for sending bulk emails"""

    def post(self, request, *args, **kwargs):
        serializer = BulkEmailSerializer(data=request.data)
        if serializer.is_valid():
            task = send_bulk_email_task.delay(
                recipient_list=serializer.validated_data['recipient_list'],
                subject=serializer.validated_data['subject'],
                message=serializer.validated_data['message'],
                html_message=serializer.validated_data.get('html_message'),
            )
            return Response({
                'task_id': task.id,
                'status': 'pending',
                'message': f'Bulk email task has been queued for {len(serializer.validated_data["recipient_list"])} recipients'
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendTemplateEmailView(APIView):
    """API view for sending emails using templates"""

    def post(self, request, *args, **kwargs):
        serializer = TemplateEmailSerializer(data=request.data)
        if serializer.is_valid():
            task = send_template_email_task.delay(
                recipient_email=serializer.validated_data['recipient_email'],
                subject=serializer.validated_data['subject'],
                template_name=serializer.validated_data['template_name'],
                context=serializer.validated_data.get('context', {}),
            )
            return Response({
                'task_id': task.id,
                'status': 'pending',
                'message': 'Template email task has been queued'
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmailWithAttachmentView(APIView):
    """API view for sending emails with attachments"""

    def post(self, request, *args, **kwargs):
        serializer = EmailWithAttachmentSerializer(data=request.data)
        if serializer.is_valid():
            task = send_email_with_attachment_task.delay(
                recipient_email=serializer.validated_data['recipient_email'],
                subject=serializer.validated_data['subject'],
                message=serializer.validated_data['message'],
                attachment_path=serializer.validated_data['attachment_path'],
                filename=serializer.validated_data.get('filename'),
                html_message=serializer.validated_data.get('html_message'),
            )
            return Response({
                'task_id': task.id,
                'status': 'pending',
                'message': 'Email with attachment task has been queued'
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailTaskStatusView(APIView):
    """API view for checking the status of an email task"""

    def get(self, request, task_id, *args, **kwargs):
        task_result = AsyncResult(task_id)

        result = {
            'task_id': task_id,
            'status': task_result.status,
        }

        if task_result.ready():
            if task_result.successful():
                result['result'] = task_result.get()
            else:
                result['error'] = str(task_result.result)

        return Response(result, status=status.HTTP_200_OK)
