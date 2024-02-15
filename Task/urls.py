from django.urls import path
from Task import views

app_name = 'task'
urlpatterns = [
    path('homepage/', views.homepage, name='homepage')
]