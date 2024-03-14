from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

from Task.models import Project

class ChatTests(TestCase):

    def setUp(self) -> None:
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**user_data)
        self.client.login(**user_data)
        project_data = {
                'project_name': 'Test Project',
                'project_description': 'Test Description',
                'creator': self.user,
                'uuid': '58609e08-66ea-4218-985b-07f1081f60ce'
            }
        project = Project(**project_data)
        project.save()
        project.users.set([self.user])
        project.save()

        self.project = project
        self.project_data = project_data

    def test_chat_view(self):
        # Login
        self.client.login(username='testuser', password='password')

        # Access the page
        chat_response = self.client.get(reverse('chat:room', kwargs={'room_name': self.project_data['uuid']}))

        self.assertEqual(chat_response.status_code, 200)
        self.assertTemplateUsed(chat_response, 'chat.html')
