from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class PersonalTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taskname = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    start_time = models.DateField()
    end_time = models.DateField()
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.taskname

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # Add related_name parameters to avoid clashes with auth.User
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True) 
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



