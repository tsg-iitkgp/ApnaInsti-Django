"""Views for upload app."""
from rest_framework import viewsets

from roles.helpers import login_required_ajax
from upload.models import UploadedImage
from upload.serializers import (Base64UploadedImageSerializer,
                                UploadedImageSerializer)


class UploadViewSet(viewsets.ModelViewSet):
    """Upload"""
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    @login_required_ajax
    def create(self, request):
        """Upload file."""
        if not request.FILES:
            self.serializer_class = Base64UploadedImageSerializer
        return super().create(request)

    @login_required_ajax
    def destroy(self, request, pk):
        """Delete file entry."""
        return super().destroy(request, pk)
