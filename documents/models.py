import os
import logging

from django.db import models

from config.vector_store import rebuild_vector_store
from .utils import extract_docx, extract_pdf

logger = logging.getLogger(__name__)


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    extracted_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()
            try:
                if ext == '.docx':
                    self.extracted_text = extract_docx(self.file.path)
                elif ext == '.pdf':
                    self.extracted_text = extract_pdf(self.file.path)
                else:
                    logger.warning(f"Unsupported file type: {ext}")
            except Exception as e:
                logger.error(f"Text extraction failed for document {self.pk}: {e}")

            Document.objects.filter(pk=self.pk).update(extracted_text=self.extracted_text)

        rebuild_vector_store()

    def __str__(self):
        return self.title
