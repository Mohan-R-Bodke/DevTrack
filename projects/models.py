from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):

    STATUS_CHOICES = [
        ('PLANNING', 'Planning'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    members = models.ManyToManyField(
        User,
        related_name='member_projects',
        blank=True
    )

    start_date = models.DateField()

    deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title