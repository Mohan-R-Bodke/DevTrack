from django import forms
from django.contrib.auth.models import User

from .models import Task
from projects.models import Project


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            'title',
            'description',
            'project',
            'assigned_to',
            'priority',
            'status',
            'due_date',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter task title'
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter task description',
                'rows': 4
            }),

            'project': forms.Select(),

            'assigned_to': forms.Select(),

            'priority': forms.Select(),

            'status': forms.Select(),

            'due_date': forms.DateInput(attrs={
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:

            # Owner's projects only.
            self.fields['project'].queryset = Project.objects.filter(
                owner=user
            ).order_by('title')

            # Default assignment.
            self.fields['assigned_to'].queryset = User.objects.filter(
                id=user.id
            )

            # When editing an existing task,
            # show members of its project.
            if self.instance and self.instance.pk:

                project = self.instance.project

                self.fields['assigned_to'].queryset = (
                    project.members.all().order_by('username')
                )

            # When creating a task with a project selected,
            # show that project's members.
            elif self.data.get('project'):

                try:

                    project_id = int(
                        self.data.get('project')
                    )

                    project = Project.objects.get(
                        id=project_id,
                        owner=user
                    )

                    self.fields['assigned_to'].queryset = (
                        project.members.all().order_by('username')
                    )

                except (
                    Project.DoesNotExist,
                    ValueError,
                    TypeError
                ):

                    pass