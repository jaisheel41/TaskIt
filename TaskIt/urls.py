"""
URL configuration for TaskIt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Task import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from django.http import HttpResponse
def test(request):
    return HttpResponse("URL Configuration is Working")


urlpatterns = [
    # path('', views.index, name='index'),
    path('test/', test),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('users/list/', views.user_list, name='user_list'),
    path('project/create/', views.create_project, name='create_project'),


    path('', include('user.urls')),
    path('task/', include('Task.urls')),
    path('admin/', admin.site.urls),
    path('homepage/', views.homepage, name='homepage'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
