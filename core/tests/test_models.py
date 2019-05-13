from django.test import TestCase
from core import models
from datetime import datetime


class ModelTests(TestCase):

    def test_file_repo_str(self):
        """
        Test the file repo model representation
        """
        filedetaobj = {
                      'file_name': "141979hello_world.txt",
                      'file_path': "textfiles",
                      'file_creation_date_time': datetime.now(),
                      'file_modification_date_time': datetime.now(),
                      'size': 167,
                      'archived': False,
                      'created_datetime': datetime.now(),
                      'updated_datetime': datetime.now(),
                      }
        filemetadata = models.RepoFiles.objects.update_or_create(**filedetaobj)
        self.assertEqual(str(filemetadata[0]), filedetaobj['file_name'])
