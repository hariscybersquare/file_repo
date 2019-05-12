from rest_framework import serializers

from core.models import RepoFiles


class RepoFilesSerializer(serializers.ModelSerializer):
    """
    Serializer for tag objects.
    """
    class Meta:
        model = RepoFiles
        fields = ('name',
                  'filepath',
                  'creationdatetime',
                  'modificationdatetime',
                  'size',
                  'archived')
