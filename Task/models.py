from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Add related_name parameters to avoid clashes with auth.User
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')
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

