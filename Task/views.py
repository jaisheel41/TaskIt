from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_protect


from Task.forms import UserProfileForm, AvatarUploadForm


# from django.urls import reverse_lazy

# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        username = request.user.username.capitalize()
        context_dict = {'username': username}
    else:
        return redirect('signIn') 

    return render(request, 'homepage.html', context=context_dict)


def user_profile(request):
    user = request.user

    context = {'user': user}
    return render(request, 'user_profile.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # 重定向到个人资料页面
    else:
        form = AvatarUploadForm(instance=request.user)
    return render(request, 'upload_avatar.html', {'form': form})