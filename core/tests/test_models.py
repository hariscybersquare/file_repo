from django.test import TestCase
from core import models
from datetime import datetime


class ModelTests(TestCase):

    def test_file_repo_str(self):
        """
        Test the file repo model representation
        """
        filedetaobj = {
                      'name': "141979hello_world.txt",
                      'filepath': "textfiles",
                      'creationdatetime': datetime.now(),
                      'modificationdatetime': datetime.now(),
                      'size': 167,
                      'archived': False
                      }
        filemetadata = models.RepoFiles.objects.update_or_create(**filedetaobj)
        self.assertEqual(str(filemetadata[0]), filedetaobj['name'])
