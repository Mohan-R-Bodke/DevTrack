from django import forms
from .models import Task
from projects.models import Project
from django.contrib.auth.models import User


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