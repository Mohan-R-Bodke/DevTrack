from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class DashboardTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='dashboarduser',
            password='password123'
        )

    def test_dashboard_requires_login(self):

        response = self.client.get(
            reverse('dashboard')
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_dashboard_authenticated(self):

        self.client.login(
            username='dashboarduser',
            password='password123'
        )

        response = self.client.get(
            reverse('dashboard')
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertContains(
            response,
            'Dashboard'
        )