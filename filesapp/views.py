from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.conf import settings

from core.models import RepoFiles
from filesapp import serializers


class FileRepoView(generics.ListAPIView):
    """
    Retrieve file metadata.
    """
    # I have added this to make the testing easy from the browser.
    if settings.AUTHENTICATION_ON:
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RepoFilesSerializer

    def get_queryset(self):
        queryset = RepoFiles.objects.all()
        archived = self.kwargs['archived']
        if archived is not None:
            queryset = queryset.filter(archived=archived)
        return queryset
