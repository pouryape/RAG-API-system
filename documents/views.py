from rest_framework import viewsets

from config.vector_store import rebuild_vector_store

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-created_at')
    serializer_class = DocumentSerializer

    def perform_destroy(self, instance):
        instance.delete()
        rebuild_vector_store()
