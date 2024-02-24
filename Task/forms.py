from django import forms
from .models import PersonalTask

class PersonalTaskForm(forms.ModelForm):
    class Meta:
        model = PersonalTask
        fields = ['taskname', 'description', 'start_time', 'end_time']

def __init__(self, *args, **kwargs):
        super(PersonalTaskForm, self).__init__(*args, **kwargs)