from django import forms
from .models import PersonalTask
from .models import CustomUser
from .models import Project
from .models import ProjectTask

class PersonalTaskForm(forms.ModelForm):
    class Meta:
        model = PersonalTask
        fields = ['taskname', 'description', 'start_time', 'end_time']

def __init__(self, *args, **kwargs):
        super(PersonalTaskForm, self).__init__(*args, **kwargs)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username']


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description']  # List all fields you want from the model
        # Optionally, you can exclude fields, but it's generally safer to explicitly list all fields you want to include.
        # exclude = ['field_to_exclude']

class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = ['project', 'taskname', 'description', 'start_time', 'end_time']