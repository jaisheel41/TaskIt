from django.test import TestCase, Client

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from Task.models import PersonalTask
from Task.forms import PersonalTaskForm
#from Task.models import UserProfile, Category, Post, Comment, Reaction
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout, update_session_auth_hash
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import PersonalTask, Notification, Project, ProjectTask

class TaskManagementTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')


    def test_homepage_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the homepage view
        response = self.client.get(reverse('task:homepage'))

        # Check if the response contains the expected username
        self.assertContains(response, 'Testuser')

    def test_create_task_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a POST request with valid data
        data = {'taskname': 'Test Task', 'description': 'Test Description', 'start_time': '2024-03-09', 'end_time': '2024-03-10'}
        response = self.client.post(reverse('task:create-task'), data)

        # Check if the response contains the task_id
        self.assertIn('task_id', response.json())

        # Check if a task has been created in the database
        self.assertEqual(PersonalTask.objects.count(), 1)

    def test_aboutus_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task:aboutus'))  # Adjust the name as per your urlconf
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aboutus.html')

    def test_calendar_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task:calendar'))  # Adjust the name as per your urlconf
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar.html')

    def test_change_password_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('change_password'))  # Adjust the name as per your urlconf
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task:user_profile'))  # Adjust the name as per your urlconf
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')

    def test_task_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task:task-list'))  # Adjust the name as per your urlconf
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personaltask.html')

    def test_fetch_notifications_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task:fetch_notifications'))  # Adjust the name as per your urlconf
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'notifications': []})

    def test_fetch_notifications_unauthenticated(self):
        response = self.client.get(reverse('fetch_notifications'))  # Adjust the name as per your urlconf
        self.assertEqual(response.status_code, 302)

    def test_create_project_post_request(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('task:create_project'), {'project_name': 'Test Project', 'project_description': 'Test Description','creator': self.id , 'users': self.id ,'uuid': '08a72b871cba421ebf236a0c5f121606' }) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

    def test_create_project_get_request(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task:create_project'))  # Adjust the name as per your urlconf
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Invalid request method'})

    def test_sign_out_view(self):
        # First, log in the user
        self.client.login(username='testuser', password='testpassword')
        # Then, test the sign-out functionality
        response = self.client.get(reverse('signOut'))
        self.assertRedirects(response, expected_url=reverse('signIn'), status_code=302)

