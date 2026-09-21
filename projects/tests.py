from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

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
        self.assertEqual(project.owner, self.user)


class ProjectViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_project_list_requires_login(self):
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 302)

    def test_project_list_authenticated(self):
        self.client.login(
            username='testuser',
            password='testpass123'
        )

        response = self.client.get(reverse('project_list'))

        self.assertEqual(response.status_code, 200)


class ProjectPermissionTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            password='password123'
        )

        self.member = User.objects.create_user(
            username='member',
            password='password123'
        )

        self.outsider = User.objects.create_user(
            username='outsider',
            password='password123'
        )

        self.project = Project.objects.create(
            title='Permission Test Project',
            description='Testing project permissions.',
            owner=self.owner,
            start_date='2026-09-17',
            deadline='2026-10-17',
            status='ACTIVE'
        )

        self.project.members.add(self.owner, self.member)

        self.api_client = APIClient()

    def test_owner_can_update_project_api(self):
        self.api_client.force_authenticate(user=self.owner)

        response = self.api_client.patch(
            f'/api/projects/{self.project.id}/',
            {'title': 'Updated Project'}
        )

        self.assertEqual(response.status_code, 200)

        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Project')

    def test_member_can_view_project_api(self):
        self.api_client.force_authenticate(user=self.member)

        response = self.api_client.get(
            f'/api/projects/{self.project.id}/'
        )

        self.assertEqual(response.status_code, 200)

    def test_member_cannot_update_project_api(self):
        self.api_client.force_authenticate(user=self.member)

        response = self.api_client.patch(
            f'/api/projects/{self.project.id}/',
            {'title': 'Member Changed Project'}
        )

        self.assertIn(response.status_code, [403, 404])

        self.project.refresh_from_db()
        self.assertEqual(
            self.project.title,
            'Permission Test Project'
        )

    def test_outsider_cannot_view_project_api(self):
        self.api_client.force_authenticate(user=self.outsider)

        response = self.api_client.get(
            f'/api/projects/{self.project.id}/'
        )

        self.assertIn(response.status_code, [403, 404])