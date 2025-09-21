from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    """Serializer for sending a single email"""
    recipient_email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    html_message = serializers.CharField(required=False, allow_null=True)


class BulkEmailSerializer(serializers.Serializer):
    """Serializer for sending bulk emails"""
    recipient_list = serializers.ListField(
        child=serializers.EmailField()
    )
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    html_message = serializers.CharField(required=False, allow_null=True)


class TemplateEmailSerializer(serializers.Serializer):
    """Serializer for sending emails using templates"""
    recipient_email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    template_name = serializers.CharField()
    context = serializers.DictField(required=False, default=dict)


class EmailWithAttachmentSerializer(serializers.Serializer):
    """Serializer for sending emails with attachments"""
    recipient_email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    attachment_path = serializers.CharField()
    filename = serializers.CharField(required=False, allow_null=True)
    html_message = serializers.CharField(required=False, allow_null=True)
