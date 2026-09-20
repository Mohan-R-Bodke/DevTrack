from django.test import TestCase
from django.contrib.auth.models import User
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

        self.assertEqual(
            task.title,
            'Test Task'
        )

        self.assertEqual(
            task.project,
            self.project
        )


class TaskSecurityTest(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            username='user1',
            password='password123'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            password='password123'
        )

        self.project = Project.objects.create(
            title='User 1 Project',
            description='Private project',
            owner=self.user1,
            start_date='2026-09-17',
            deadline='2026-10-17',
            status='ACTIVE'
        )

    def test_user_cannot_see_other_user_tasks(self):

        Task.objects.create(
            title='Private Task',
            project=self.project,
            assigned_to=self.user1,
            priority='HIGH',
            status='TODO',
            due_date='2026-09-25'
        )

        self.client.login(
            username='user2',
            password='password123'
        )

        response = self.client.get(
            '/api/tasks/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.data),
            0
        )