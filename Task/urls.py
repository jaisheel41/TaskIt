from django.urls import path
from Task import views
from .views import user_profile

app_name = 'task'
urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('user/profile/', user_profile, name='user_profile'),
]
