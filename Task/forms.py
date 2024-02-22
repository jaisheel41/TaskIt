from django import forms
from .models import PersonalTask

class PersonalTaskForm(forms.ModelForm):
    class Meta:
        model = PersonalTask
        fields = ['taskname', 'description', 'start_time', 'end_time', 'status']

from django import forms
from .models import CustomUser


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username']


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']
