import os

from rest_framework import serializers

from .models import Document

ALLOWED_EXTENSIONS = {'.docx', '.pdf'}


class DocumentSerializer(serializers.ModelSerializer):
    extracted_text = serializers.CharField(read_only=True)

    class Meta:
        model = Document
        fields = '__all__'

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                f"Unsupported file type '{ext}'. Only .docx and .pdf files are accepted."
            )
        return value
