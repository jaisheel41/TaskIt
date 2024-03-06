from django.urls import path
from Task import views


app_name = 'task'
urlpatterns = [
    path('projectmanagement/', views.projectmanagement, name='projectmanagement'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/update/<int:project_id>/', views.update_project, name='update-project'),
    path('project/delete/<int:project_id>/', views.delete_project, name='delete-project'),

    path('personaltask/', views.task_list, name='task-list'),
    path('create/', views.create_task, name='create-task'),
    path('homepage/', views.homepage, name='homepage'),
    path('update/<int:task_id>/', views.update_task, name='update-task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete-task'),
    path('users/list/', views.user_list, name='user_list'),

]
