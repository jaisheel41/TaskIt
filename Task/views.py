from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
# from django.urls import reverse_lazy

# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        username = request.user.username.capitalize()
        context_dict = {'username': username}
    else:
        return redirect('task:homepage') 

    return render(request, 'homepage.html', context=context_dict)
