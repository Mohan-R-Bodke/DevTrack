from rest_framework import serializers
from .models import Task
from projects.models import Project


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task

        fields = [
            'id',
            'title',
            'description',
            'project',
            'assigned_to',
            'priority',
            'status',
            'due_date',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate_title(self, value):

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Task title must contain at least 3 characters."
            )

        return value.strip()

    def validate_project(self, project):

        request = self.context['request']

        if project.owner != request.user:

            raise serializers.ValidationError(
                "You cannot add a task to another user's project."
            )

        return project