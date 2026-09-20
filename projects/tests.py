from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project


class ProjectModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_project_creation(self):

        project = Project.objects.create(
            title='Test Project',
            description='Testing DevTrack project functionality.',
            owner=self.user,
            start_date='2026-09-17',
            deadline='2026-10-17',
            status='ACTIVE'
        )

        self.assertEqual(project.title, 'Test Project')

        self.assertEqual(
            project.owner,
            self.user
        )


class ProjectViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_project_list_requires_login(self):

        response = self.client.get(
            reverse('project_list')
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_project_list_authenticated(self):

        self.client.login(
            username='testuser',
            password='testpass123'
        )

        response = self.client.get(
            reverse('project_list')
        )

        self.assertEqual(
            response.status_code,
            200
        )