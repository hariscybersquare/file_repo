from django.db import models


class RepoFiles(models.Model):
    """
    Model for the RepoFiles.
    """
    class Meta:
        db_table = 'file_repo'
    file_name = models.CharField(max_length=255, primary_key=True)
    file_path = models.CharField(max_length=255)
    file_creation_date_time = models.DateTimeField(null=False)
    file_modification_date_time = models.DateTimeField(null=False)
    size = models.IntegerField(null=False)
    archived = models.BooleanField(null=False)
    created_datetime = models.DateTimeField(null=False)
    updated_datetime = models.DateTimeField(null=False)

    def __str__(self):
        return self.file_name
