from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile
import random


def index(request):
    if request.user.is_authenticated:
        return redirect('Home')
    else:
        return redirect('signIn')


class Sign_In(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Home')
        else:
            return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')

        else:
            response = JsonResponse({"error": "Invalid Credentials"})
            response.status_code = 403
            return response


class Sign_Up(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Home')
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

            return redirect('Home')

        except:
            response = JsonResponse({"error": "Duplicate User or Server error"})
            response.status_code = 403
            return response


class Sign_Out(View):
    def get(self, request):
        logout(request)
        return redirect('signIn')
