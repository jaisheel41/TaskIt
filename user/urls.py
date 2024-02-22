from django.urls import path
from .views import Sign_In, Sign_Up, index, Sign_Out
# from .views import home
from .views import CustomLogoutView
from .views import login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', index, name='index'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # path('', home, name='homepage'),
    path('signIn', Sign_In.as_view(), name="signIn"),
    path('signUp', Sign_Up.as_view(), name='signUp'),
    path('signOut', Sign_Out.as_view()),
]
