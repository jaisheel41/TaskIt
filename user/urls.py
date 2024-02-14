from django.urls import path
from .views import Sign_In, Sign_Up, index, Sign_Out

urlpatterns = [
    path('', index, name='index'),
    path('signIn', Sign_In.as_view(), name="signIn"),
    path('signUp', Sign_Up.as_view(), name='signUp'),
    path('signOut', Sign_Out.as_view())
]