from django.db import models


class RepoFiles(models.Model):
    """
    Model for the RepoFiles.
    """
    class Meta:
        db_table = 'file_repo'
    name = models.CharField(max_length=255, primary_key=True)
    filepath = models.CharField(max_length=255)
    creationdatetime = models.DateTimeField()
    modificationdatetime = models.DateTimeField()
    size = models.IntegerField()
    archived = models.BooleanField()

    def __str__(self):
        return self.name
