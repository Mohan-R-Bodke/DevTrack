from django import forms
from django.contrib.auth.models import User

from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            'title',
            'description',
            'members',
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
                'rows': 5
            }),

            'members': forms.CheckboxSelectMultiple(),

            'start_date': forms.DateInput(attrs={
                'type': 'date'
            }),

            'deadline': forms.DateInput(attrs={
                'type': 'date'
            }),

            'status': forms.Select(),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:

            self.fields['members'].queryset = (
                User.objects
                .exclude(id=user.id)
                .order_by('username')
            )