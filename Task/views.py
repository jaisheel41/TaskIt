from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PersonalTask
from django.views.decorators.http import require_POST
from .forms import PersonalTaskForm, ProjectForm
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Project
# from django.urls import reverse_lazy
from .models import Project, User
#from .forms import ProjectForm  # Import your project form



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