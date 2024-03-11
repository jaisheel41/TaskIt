from django.urls import path
from chat import views

app_name = 'chat'
urlpatterns = [
    #path('<uuid:room_name>/', views.chat, name='room'),
    path('ajax/<str:room_name>/', views.chat_ajax, name='room_ajax'),
    path('send-message/', views.send_message, name='send_message'),
    path('update/', views.update, name='update')
]
