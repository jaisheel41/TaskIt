from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile
import random
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        return redirect('task:homepage') 
    else:
        return redirect('signIn')


class Sign_In(View):
    def get(self, request):
        if request.user.is_authenticated:
            # return redirect('homepage.html')
            return redirect('task:homepage') 
        else:
            return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task:homepage') 

        else:
            response = JsonResponse({"error": "Invalid Credentials"})
            response.status_code = 403
            return response


class Sign_Up(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('task:homepage') 
        else:
            return redirect('signIn')

    def post(self, request):
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.create_user(username, email, password)
            user.save()

            login(request, user)

            n = random.randint(16, 45)
            pf_url = f'/media/users/{n}.jpg'
            pf = Profile(user=user, profile_photo=pf_url)
            pf.save()

            return redirect('task:homepage') 

        except:
            response = JsonResponse({"error": "Duplicate User or Server error"})
            response.status_code = 403
            return response


class Sign_Out(View):
    def get(self, request):
        logout(request)
        return redirect('signIn')

# def home(request):
#     return render(request, 'homepage.html')
    

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

def login_view(request):
    return render(request, 'login.html')