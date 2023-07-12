from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Message

class IntegrationTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.message = Message.objects.create(sender=self.user, recipient=self.user, body='Test message')
    
    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('inbox'))
        print("Test login_view passed.")
    
    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        print("Test logout_view passed.")
    
    def test_inbox_view_authenticated(self):
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox.html')
        print("Test inbox_view (authenticated) passed.")
    
    def test_inbox_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('inbox'))
        self.assertRedirects(response, reverse('login'))
        print("Test inbox_view (unauthenticated) passed.")
    
    # def test_chat_view_authenticated(self):
    #     response = self.client.get(reverse('chat_view'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertJSONEqual(str(response.content, encoding='utf-8'), {'messages': [{'id': self.message.id, 'sender': self.user.id, 'recipient': self.user.id, 'body': 'Test message', 'created_at': self.message.created_at.isoformat()}]})
    #     print("Test chat_view (authenticated) passed.")
    
    # def test_chat_view_unauthenticated(self):
    #     self.client.logout()
    #     response = self.client.get(reverse('chat_view'))
    #     self.assertRedirects(response, reverse('login'))
    #     print("Test chat_view (unauthenticated) passed.")
    
    def test_delete_message_authenticated(self):
        response = self.client.post(reverse('delete_message', args=[self.message.id]))
        self.assertRedirects(response, reverse('inbox'))
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())
        print("Test delete_message (authenticated) passed.")
    
    def test_delete_message_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('delete_message', args=[self.message.id]))
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(Message.objects.filter(id=self.message.id).exists())
        print("Test delete_message (unauthenticated) passed.")
    
    def test_compose_message_authenticated(self):
        response = self.client.post(reverse('compose'), {'recipient': 'testuser', 'body': 'Test message'})
        self.assertRedirects(response, reverse('inbox'))
        self.assertEqual(Message.objects.count(), 2)
        print("Test compose_message (authenticated) passed.")
    
    def test_compose_message_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('compose'), {'recipient': 'testuser', 'body': 'Test message'})
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Message.objects.count(), 1)
        print("Test compose_message (unauthenticated) passed.")
    
    def test_edit_message_authenticated(self):
        response = self.client.post(reverse('edit_message', args=[self.message.id]), {'recipient': 'testuser', 'body': 'Updated message'})
        self.assertRedirects(response, reverse('inbox'))
        self.message.refresh_from_db()
        self.assertEqual(self.message.body, 'Updated message')
        print("Test edit_message (authenticated) passed.")
    
    def test_edit_message_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('edit_message', args=[self.message.id]), {'recipient': 'testuser', 'body': 'Updated message'})
        self.assertRedirects(response, reverse('login'))
        self.message.refresh_from_db()
        self.assertEqual(self.message.body, 'Test message')
        print("Test edit_message (unauthenticated) passed.")
