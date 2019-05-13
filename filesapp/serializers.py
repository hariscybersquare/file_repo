from rest_framework import serializers

from core.models import RepoFiles


class RepoFilesSerializer(serializers.ModelSerializer):
    """
    Serializer for tag objects.
    """
    class Meta:
        model = RepoFiles
        fields = ('file_name',
                  'file_path',
                  'file_creation_date_time',
                  'file_modification_date_time',
                  'size',
                  'archived',
                  'created_datetime',
                  'updated_datetime')
