from django.urls import path
from Task import views
# from .views import user_profile

app_name = 'task'
urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/profilesv/', views.profilesv, name='profilesv'),
]
