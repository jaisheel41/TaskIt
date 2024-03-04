from django import forms
from .models import PersonalTask
from .models import CustomUser

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