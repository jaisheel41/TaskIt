from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile
import random
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomPasswordChangeForm





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
            # remember_me = request.POST.get('remember_me', False)
            # if remember_me:
            #     # Set session to expire after 2 weeks
            #     request.session.set_expiry(1209600)  # 2 weeks in seconds
            # else:
            #     # Set session to expire at browser close
            #     request.session.set_expiry(0)
            
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

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            user = User.objects.create_user(username, email, password)
            user.save()

            login(request, user)

            # n = random.randint(16, 45)
            # pf_url = f'/media/users/{n}.jpg'
            # pf = Profile(user=user, profile_photo=pf_url)
            # pf.save()

            return redirect('task:homepage') 

        except IntegrityError as e:
            response = JsonResponse({"error": "Duasdasdas User"}, status=400)
            return response
        except ValidationError as e:
            response = JsonResponse({"error": str(e)}, status=400)
            return response
        except Exception as e:
            # For any other exceptions, send an internal server error response
            response = JsonResponse({"error": "sersdsdd error"}, status=500)
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
        return redirect('signIn')

def login_view(request):
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomPasswordChangeForm

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'success': True})
        else:
            # Collect the errors into a list (or any other structure you see fit)
            errors = list(form.errors.values())
            return JsonResponse({'success': False, 'error': errors}, status=400)
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
