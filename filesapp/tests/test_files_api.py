from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import RepoFiles

from filesapp.serializers import RepoFilesSerializer
from datetime import datetime


class PublicRepoFilesApiTests(TestCase):
    """
    Test the publicly available Tags API.
    """
    def setUp(self):
        self.client = APIClient()

    def test_login_required_for_get(self):
        """
        Test for checking login required for get request

        """
        res = self.client.get(reverse('getfiles', kwargs={'archived': True}))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRepoFilesTests(TestCase):
    """
    Test the authorized API calls for repofile
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'haris.np@gmail.com', '12345'
            )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_non_archived_files_only(self):
        """
        Test non archived files retrieval.
        """
        RepoFiles.objects.create(
            file_name="141980hello_world.txt",
            file_path="filetest/textfiles",
            file_creation_date_time="2019-05-10 18:28:53.162",
            file_modification_date_time="2019-05-05 13:28:53",
            size=167,
            archived=True,
            created_datetime=datetime.now(),
            updated_datetime=datetime.now())
        RepoFiles.objects.create(
            file_name="141979hello_world.txt",
            file_path="filetest/textfiles",
            file_creation_date_time="2019-05-10 18:28:53.162",
            file_modification_date_time="2019-05-05 13:28:53",
            size=167,
            archived=True,
            created_datetime=datetime.now(),
            updated_datetime=datetime.now())

        repofiles = RepoFiles.objects.all()
        serializer = RepoFilesSerializer(repofiles, many=True)
        res = self.client.get(reverse('getfiles', kwargs={'archived': True}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_archived_files_only(self):
        """
        Test archived files retrieval.
        """
        RepoFiles.objects.create(
            file_name="141979hello_world.txt",
            file_path="filetest/textfiles",
            file_creation_date_time="2019-05-10 18:28:53.162",
            file_modification_date_time="2019-05-05 13:28:53",
            size=167,
            archived=False,
            created_datetime=datetime.now(),
            updated_datetime=datetime.now())
        RepoFiles.objects.create(
                    file_name="141995hello_world.txt",
                    file_path="filetest/textfiles",
                    file_creation_date_time="2019-05-10 18:28:53.162",
                    file_modification_date_time="2019-05-05 13:28:53",
                    size=167,
                    archived=False,
                    created_datetime=datetime.now(),
                    updated_datetime=datetime.now())

        repofiles = RepoFiles.objects.all()
        serializer = RepoFilesSerializer(repofiles, many=True)
        res = self.client.get(reverse('getfiles', kwargs={'archived': False}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_non_archived_files(self):
        """
        Test non archived files retrieval where the database has both archived
        and non archived files.
        """
        RepoFiles.objects.create(
            file_name="141979hello_world.txt",
            file_path="filetest/textfiles",
            file_creation_date_time="2019-05-10 18:28:53.162",
            file_modification_date_time="2019-05-05 13:28:53",
            size=167,
            archived=True,
            created_datetime=datetime.now(),
            updated_datetime=datetime.now())
        RepoFiles.objects.create(
            file_name="141989hello_world.txt",
            file_path="filetest/textfiles",
            file_creation_date_time="2019-05-10 18:28:53.162",
            file_modification_date_time="2019-05-05 13:28:53",
            size=167,
            archived=True,
            created_datetime=datetime.now(),
            updated_datetime=datetime.now())
        RepoFiles.objects.create(
            file_name="1419100hello_world.txt",
            file_path="filetest/textfiles",
            file_creation_date_time="2019-05-10 18:28:53.162",
            file_modification_date_time="2019-05-05 13:28:53",
            size=167,
            archived=False,
            created_datetime=datetime.now(),
            updated_datetime=datetime.now())

        repofiles = RepoFiles.objects.filter(archived=True)
        serializer = RepoFilesSerializer(repofiles, many=True)
        res = self.client.get(reverse('getfiles', kwargs={'archived': True}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
