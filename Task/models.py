from django.db import models
from django.contrib.auth.models import User

class PersonalTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taskname = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    start_time = models.DateField()
    end_time = models.DateField()
    status = models.CharField(max_length=1)

    def __str__(self):
        return self.taskname
