from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PersonalTask
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
import json
from .forms import PersonalTaskForm
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
# from django.urls import reverse_lazy
from django.contrib.auth.models import User
from Task.forms import UserProfileForm, AvatarUploadForm

# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        username = request.user.username.capitalize()
        context_dict = {'username': username}
    else:
        return redirect('signIn') 

    return render(request, 'homepage.html', context=context_dict)

def task_list(request):
    if not request.user.is_authenticated:
        return redirect('signIn')
        
    tasks = PersonalTask.objects.filter(user=request.user)
    return render(request, 'personaltask.html', {'tasks': tasks})

@require_POST
def create_task(request):
    form = PersonalTaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return JsonResponse({'task_id': task.id})
    else:
        return JsonResponse({'error': form.errors}, status=400)
    
def update_task(request, task_id):
    task = get_object_or_404(PersonalTask, pk=task_id, user=request.user)
    if request.method == 'POST':
        form = PersonalTaskForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)  # Don't commit yet
            updated_task.status = request.POST.get('status', 0)  # Default to 0 if not provided
            updated_task = form.save()
            task_data = model_to_dict(updated_task)
            task_data['end_time'] = updated_task.end_time.strftime('%b %d, %Y')
            return JsonResponse({'task': task_data}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(PersonalTask, id=task_id, user=request.user)
    task.delete()
    return JsonResponse({'status': 'success'})

@require_http_methods(["GET"])
def get_task_status(request, task_id):
    # Replace 'Task' with your actual Task model
    task = get_object_or_404(PersonalTask, pk=task_id)
    # Assuming the Task model has a field called 'status' that holds the progress
    task_status = task.status
    
    # Return the status as JSON
    return JsonResponse({'taskStatus': task_status})

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
                    with open(f"./static/media/images/{request.user.id}.jpg", 'wb+') as f:
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
            return redirect('profile')
    else:
        form = AvatarUploadForm(instance=request.user)
    return render(request, 'upload_avatar.html', {'form': form})

@login_required
def calendar_view(request):
    tasks = PersonalTask.objects.filter(user=request.user).values(
        'id', 'taskname', 'end_time', 'status', 'description'  # Assuming 'status' is the progress percentage
    )

    tasks_for_calendar = [
        {
            'title': task['taskname'],
            'start': task['end_time'].isoformat(),
            'allDay': True,
            'extendedProps': {
                'description': task['description'],
                'status': task['status']  # Progress percentage
            }
        } for task in tasks
    ]

    tasks_json = json.dumps(tasks_for_calendar)
    return render(request, 'calendar.html', {'tasks_json': tasks_json})
