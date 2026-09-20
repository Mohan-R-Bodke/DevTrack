from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project

        fields = [
            'id',
            'title',
            'description',
            'owner',
            'start_date',
            'deadline',
            'status',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'owner',
            'created_at',
        ]

    def validate_title(self, value):

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Project title must contain at least 3 characters."
            )

        return value.strip()

    def validate(self, data):

        start_date = data.get('start_date')
        deadline = data.get('deadline')

        if start_date and deadline:

            if deadline < start_date:
                raise serializers.ValidationError(
                    "Deadline cannot be before the start date."
                )

        return data