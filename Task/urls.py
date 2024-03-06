from django.urls import path
from Task import views
from .views import get_task_status

app_name = 'task'
urlpatterns = [
    path('personaltask/', views.task_list, name='task-list'),
    path('create/', views.create_task, name='create-task'),
    path('homepage/', views.homepage, name='homepage'),
    path('update/<int:task_id>/', views.update_task, name='update-task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete-task'),
    path('get-task-status/<int:task_id>/', get_task_status, name='get_task_status'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/profilesv/', views.profilesv, name='profilesv'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('user/check_avatar/', views.check_avatar, name='check_avatar'),
]
