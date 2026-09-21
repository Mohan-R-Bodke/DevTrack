from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from projects.models import Project
from .models import Task


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.project = Project.objects.create(
            title='Test Project',
            description='Testing project',
            owner=self.user,
            start_date='2026-09-17',
            deadline='2026-10-17',
            status='ACTIVE'
        )

    def test_task_creation(self):
        task = Task.objects.create(
            title='Test Task',
            description='Testing task functionality.',
            project=self.project,
            assigned_to=self.user,
            priority='HIGH',
            status='TODO',
            due_date='2026-09-25'
        )

        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.project, self.project)


class TaskSecurityTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            password='password123'
        )

        self.member = User.objects.create_user(
            username='member',
            password='password123'
        )

        self.other_member = User.objects.create_user(
            username='othermember',
            password='password123'
        )

        self.outsider = User.objects.create_user(
            username='outsider',
            password='password123'
        )

        self.project = Project.objects.create(
            title='User 1 Project',
            description='Private project',
            owner=self.owner,
            start_date='2026-09-17',
            deadline='2026-10-17',
            status='ACTIVE'
        )

        self.project.members.add(
            self.owner,
            self.member,
            self.other_member
        )

        self.task = Task.objects.create(
            title='Private Task',
            description='Task description',
            project=self.project,
            assigned_to=self.member,
            priority='HIGH',
            status='TODO',
            due_date='2026-09-25'
        )

        self.api_client = APIClient()

    def test_outsider_cannot_see_other_user_tasks(self):
        self.api_client.force_authenticate(
            user=self.outsider
        )

        response = self.api_client.get('/api/tasks/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_project_member_can_view_all_project_tasks(self):
        self.api_client.force_authenticate(
            user=self.other_member
        )

        response = self.api_client.get('/api/tasks/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['title'],
            'Private Task'
        )

    def test_assigned_member_can_update_task_status(self):
        self.api_client.force_authenticate(
            user=self.member
        )

        response = self.api_client.patch(
            f'/api/tasks/{self.task.id}/',
            {'status': 'IN_PROGRESS'}
        )

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.status,
            'IN_PROGRESS'
        )

    def test_unassigned_member_cannot_update_task(self):
        self.api_client.force_authenticate(
            user=self.other_member
        )

        response = self.api_client.patch(
            f'/api/tasks/{self.task.id}/',
            {'status': 'COMPLETED'}
        )

        self.assertEqual(response.status_code, 403)

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.status,
            'TODO'
        )

    def test_assigned_member_cannot_change_task_details(self):
        self.api_client.force_authenticate(
            user=self.member
        )

        response = self.api_client.patch(
            f'/api/tasks/{self.task.id}/',
            {
                'title': 'Changed By Member',
                'status': 'IN_PROGRESS'
            }
        )

        self.assertEqual(response.status_code, 403)

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.title,
            'Private Task'
        )

    def test_project_owner_can_edit_task(self):
        self.api_client.force_authenticate(
            user=self.owner
        )

        response = self.api_client.patch(
            f'/api/tasks/{self.task.id}/',
            {
                'title': 'Owner Updated Task',
                'priority': 'MEDIUM'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.title,
            'Owner Updated Task'
        )

    def test_outsider_cannot_access_specific_task(self):
        self.api_client.force_authenticate(
            user=self.outsider
        )

        response = self.api_client.get(
            f'/api/tasks/{self.task.id}/'
        )

        self.assertIn(response.status_code, [403, 404])