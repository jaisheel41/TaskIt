from django.urls import path
from .views import Sign_In, Sign_Up, index, Sign_Out
# from .views import home
from .views import CustomLogoutView
from .views import login_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signIn/', login_view, name='login'),
    path('', index, name='index'),
    path('logout/', Sign_Out.as_view(), name='logout'),
    # path('', home, name='homepage'),
    path('signIn', Sign_In.as_view(), name="signIn"),
    path('signUp', Sign_Up.as_view(), name='signUp'),
    path('signOut', Sign_Out.as_view(), name="signOut"),
]
