from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PersonalTask
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
import json
from .forms import PersonalTaskForm, ProjectTaskForm
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
# from django.urls import reverse_lazy
from django.contrib.auth.models import User
from Task.forms import UserProfileForm, AvatarUploadForm
from .models import Notification
from django.views.decorators.csrf import csrf_exempt
from .models import Project
from .forms import ProjectForm
from .models import ProjectTask

from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PersonalTask
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

from .forms import PersonalTaskForm
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
# from django.urls import reverse_lazy
from django.contrib.auth.models import User
from Task.forms import UserProfileForm, AvatarUploadForm
import os

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
        # Create and save a notification
        create_notification(request.user, "Task Creation", f"Task '{task.taskname}' has been created.")

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

def user_profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'user_profile.html', context)


import os

def profilesv(request):
    user = request.user
    context = {'user': user}

    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        form = UserProfileForm(request.POST, instance=user)
        new_email = request.POST.get('email')
        new_username = request.POST.get('username')
        if (User.objects.filter(username=new_username).exists() and new_username != user.username) or \
           (User.objects.filter(email=new_email).exists() and new_email != user.email):
            return JsonResponse({'success': False, 'message': 'Error: Username or email already exists!!'})
        else:
            user.username = new_username
            user.email = new_email
            user.save()
            
            if not form.errors:
                form.save()

                if avatar is not None:

              

                    # Assuming 'static' is at your Django project root level
                    user_pic_dir = os.path.join('static', 'media', 'userpic')
                    os.makedirs(user_pic_dir, exist_ok=True)  # Make sure the directory exists

                    with open(os.path.join(user_pic_dir, f"{request.user.id}.jpg"), 'wb+') as f:

                        for chunk in avatar.chunks():
                            f.write(chunk)

                # Create and save a notification
                create_notification(user, "Profile Update", "Your profile has been updated successfully.")

                return JsonResponse({'success': True, 'message': 'Modified successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Incorrect format!!!'})
    return redirect(user_profile, context)

def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AvatarUploadForm(instance=request.user)
    return render(request, 'upload_avatar.html', {'form': form})

def check_avatar(request):
    if request.method == 'GET':
        user_id = request.user.id

        if str(user_id)+'.jpg' in os.listdir('./static/media/UserPic/'):
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

@login_required
def notification_view(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    context = {
        'notifications': notifications
    }
    return render(request, 'notification.html', context)



def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        return JsonResponse({"notifications": list(notifications.values())})
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)

@login_required
def fetch_notifications(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return JsonResponse({'notifications': list(notifications.values())})


def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)

@login_required
@require_POST
def clear_notifications(request):
    request.user.notifications.filter(is_read=True).delete()
    return JsonResponse({'status': 'success'})

def create_notification(user, title, message):
    notification = Notification(user=user, title=title, message=message)
    notification.save()
        
def my_custom_404_view(request, exception):
    return render(request, '404.html', {}, status=404)



def projectmanagement(request):
    if not request.user.is_authenticated:
        return redirect('signIn')

    users = User.objects.all()  # Get all user objects
    projects = Project.objects.filter(users=request.user)  # Replace with your actual query to get projects

    # Pass both users and projects to the template context
    context = {
        'users': users,
        'projects': projects,
    }

    return render(request, 'projectmanagement.html', context)


def user_list(request):
    users = User.objects.all().values_list('id', flat=True)  # 获取所有用户的ID
    return JsonResponse(list(users), safe=False)


@csrf_exempt
def create_project(request):
    if request.method == 'POST':
        # Get the form data
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        #project_details = request.POST.get('project_details')

        # Handle multi-selected users
        user_ids = [value for key, value in request.POST.items() if key.startswith('project_users_')]

        # Create a project instance
        project = Project(
            project_name=project_name,
            project_description=project_description,
            #project_details=project_details,
        )
        project.save()

        user_ids = [value for key, value in request.POST.items() if key.startswith('project_users_')]
        for user_id in user_ids:
            user = User.objects.get(pk=user_id)
            project.users.add(user)

        project.save()
        # TODO: Add users to the project (update your project model accordingly)

        return JsonResponse({'status': 'success'})
    else:
        # Handle non-POST requests here
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# Update Project
@login_required
@require_POST
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id, users=request.user)  # Ensure the user has access
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        updated_project = form.save(commit=False)
        updated_project.save()
        form.save_m2m()  # Save many-to-many data for the form
        project_data = model_to_dict(updated_project, fields=[field.name for field in updated_project._meta.fields])
        return JsonResponse({'status': 'success', 'project': project_data})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})

# Delete Project
@login_required
@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, users=request.user)
    project.delete()
    return JsonResponse({'status': 'success'})


def project_task_list(request, project_uuid):
    if not request.user.is_authenticated:
        return redirect('signIn')
    
    if not Project.objects.get(uuid=project_uuid):
        return redirect('task:homepage')
    
    context_dict = {}
    tasks = ProjectTask.objects.filter(project=Project.objects.get(uuid=project_uuid))
    context_dict.update({'tasks': tasks})
    #context_dict.update({'header': project_id})
    context_dict.update({'header': Project.objects.get(uuid=project_uuid).project_name})
    context_dict.update({'uuid': project_uuid})
    context_dict.update({'project_id': Project.objects.get(uuid=project_uuid).id})
    return render(request, 'projecttask.html', context_dict)

@require_POST
def create_project_task(request, project_uuid):
    form = ProjectTaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        #task.user = request.user
        task.project = Project.objects.get(uuid=project_uuid)
        task.save()
        return JsonResponse({'task_id': task.id})
    else:
        return JsonResponse({'error': form.errors}, status=400)
    
def update_project_task(request, project_uuid, project_task_id):
    task = get_object_or_404(ProjectTask, pk=project_task_id, project=Project.objects.get(uuid=project_uuid))
    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, instance=task)
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
def delete_project_task(request, project_uuid, project_task_id):
    task = get_object_or_404(ProjectTask, id=project_task_id, project=Project.objects.get(uuid=project_uuid))
    task.delete()
    return JsonResponse({'status': 'success'})