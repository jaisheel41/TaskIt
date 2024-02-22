from django.urls import path
from Task import views
# from .views import user_profile

app_name = 'task'
urlpatterns = [
    path('personaltask/', views.task_list, name='task-list'),
    path('create/', views.create_task, name='create-task'),
    path('homepage/', views.homepage, name='homepage'),
    path('update/<int:task_id>/', views.update_task, name='update-task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete-task')
]
