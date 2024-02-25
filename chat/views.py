from django.shortcuts import render

# Create your views here.
def chat(request, room_name):
    username = request.user.username
    return render(request, "chat.html", {
        "room_name": room_name,
        "username": username
    })