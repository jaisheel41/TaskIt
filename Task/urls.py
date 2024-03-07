from django.urls import path
from Task import views
from .views import get_task_status
from .views import notification_view
from .views import get_notifications
from .views import fetch_notifications, mark_notification_read
from . import views
from .views import clear_notifications




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
    path('notifications/', notification_view, name='notifications'),
    # path('notifications/', get_notifications, name='notifications'),
    path('notifications/fetch/', views.fetch_notifications, name='fetch_notifications'),
    path('notifications/read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path('notifications/clear/', clear_notifications, name='clear_notifications'),
    
    path('projectmanagement/', views.projectmanagement, name='projectmanagement'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/update/<int:project_id>/', views.update_project, name='update-project'),
    path('project/delete/<int:project_id>/', views.delete_project, name='delete-project'),

]
