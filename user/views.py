

from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from .models import Profile
import random
from django.contrib import messages
from .forms import CustomPasswordChangeForm
from Task.views import create_notification

def index(request):
    """
    Index view to redirect authenticated users to the homepage and others to the sign-in page.
    """
    if request.user.is_authenticated:
        return redirect('task:homepage') 
    else:
        return redirect('signIn')

class Sign_In(View):
    """
    Sign-in view for handling user authentication.
    """
    def get(self, request):
        if request.user.is_authenticated:
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
            # Return error response for invalid credentials
            response = JsonResponse({"error": "Invalid Credentials"})
            response.status_code = 403
            return response

class Sign_Up(View):
    """
    Sign-up view for creating new user accounts.
    """
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
            return redirect('task:homepage') 

        except:
            # Return error response for duplicate user or server error
            response = JsonResponse({"error": "Duplicate User or Server error"})
            response.status_code = 403
            return response

class Sign_Out(View):
    """
    Sign-out view for logging out users.
    """
    def get(self, request):
        logout(request)
        return redirect('signIn')

class CustomLogoutView(View):
    """
    Custom logout view for logging out users and redirecting to the sign-in page.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('signIn')

def login_view(request):
    """
    Simple login view rendering the login page.
    """
    return render(request, 'login.html')

def change_password(request):
    """
    View for handling password change requests.
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            # Create and save a notification for successful password change
            create_notification(user, "Password Change", "Your password has been successfully changed.")

            return JsonResponse({'success': True})
        else:
            # Return error response for invalid form submissions
            errors = list(form.errors.values())
            return JsonResponse({'success': False, 'error': errors}, status=400)
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})