from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
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


def profilesv(request):
    user = request.user
    context = {'user': user}
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        form = UserProfileForm(request.POST, instance=request.user)
        new_email = request.POST.get('email')
        new_username = request.POST.get('username')

        if (User.objects.filter(username=new_username).exists() and new_username != user.username) or \
                (User.objects.filter(email=new_email).exists() and new_email != user.email):

            return JsonResponse({'success': False, 'message': 'Error: Username or email already exists!!'})
        else:
            request.user.username = new_username
            request.user.email = new_email
            request.user.save()
            if not form.errors:
                form.save()

                if avatar is not None:
                    with open(f"./static/media/images/{new_username}.jpg", 'wb+') as f:
                        for chunk in avatar:
                            f.write(chunk)
                form.save()
                return JsonResponse({'success': True, 'message': 'Modified successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Incorrect format!!!'})

    return redirect(user_profile)


def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # 重定向到个人资料页面
    else:
        form = AvatarUploadForm(instance=request.user)
    return render(request, 'upload_avatar.html', {'form': form})
