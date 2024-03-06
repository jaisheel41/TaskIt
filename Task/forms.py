from django import forms
from .models import PersonalTask
from .models import Project

class PersonalTaskForm(forms.ModelForm):
    class Meta:
        model = PersonalTask
        fields = ['taskname', 'description', 'start_time', 'end_time', 'status']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description']  # List all fields you want from the model
        # Optionally, you can exclude fields, but it's generally safer to explicitly list all fields you want to include.
        # exclude = ['field_to_exclude']