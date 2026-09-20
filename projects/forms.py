from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'start_date',
            'deadline',
            'status',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter project title'
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter project description',
                'rows': 4
            }),

            'start_date': forms.DateInput(attrs={
                'type': 'date'
            }),

            'deadline': forms.DateInput(attrs={
                'type': 'date'
            }),

            'status': forms.Select(),
        }