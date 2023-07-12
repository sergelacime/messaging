
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from webtest import TestApp
from .models import Message
from messagerie_app.wsgi import application

class MessagingIntegrationTests(TestCase):
    def setUp(self):
        # Initialisation de l'application WebTest avec l'application Django
        self.app = TestApp(application)

        # Création d'un utilisateur de test
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        first_user = User.objects.all().first()
        last_user = User.objects.all().last()


        # Création d'un message de test
        self.message = Message.objects.create(sender=self.user, recipient=first_user, body='Message de test')
        last_message = Message.objects.all().last()

        print("\n\nUtilisateur test : "+ str(last_user.username) +"\nMessage test : "+ str(last_message.body) +"\n à "+str(last_message.recipient))


    def test_login_and_inbox(self):
        # Vérification de la page de connexion
        response = self.app.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Tentative de connexion avec l'utilisateur de test
        response = self.app.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('inbox'))

        # Vérification de la page de boîte de réception après la connexion réussie
        response = self.app.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test', response)


    # def test_delete_message(self):
    #     # Connexion avec l'utilisateur de test
    #     self.app.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

    #     # Suppression du message de test
    #     response = self.app.get(reverse('delete_message', args=[self.message.id]))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('inbox'))

    #     # Vérification que le message a bien été supprimé
    #     self.assertFalse(Message.objects.filter(id=self.message.id).exists())


    # def test_compose_and_edit_message(self):
    #     # Connexion avec l'utilisateur de test
    #     self.app.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

    #     # Création d'un nouveau message
    #     response = self.app.get(reverse('compose'))
    #     self.assertEqual(response.status_code, 200)

    #     response = self.app.post(reverse('compose'), {
    #         'recipient': 'testuser',
    #         'body': 'New Test body',
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('inbox'))

    #     # Récupération du message créé
    #     message = Message.objects.get(recipient= 'testuser',)

    #     # Modification du message
    #     response = self.app.get(reverse('edit_message', args=[message.id]))
    #     self.assertEqual(response.status_code, 200)

    #     response = self.app.post(reverse('edit_message', args=[message.id]), {
    #         'recipient': 'testuser',
    #         'body': 'Modified Test body',
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, reverse('inbox'))

    #     # Vérification que le message a bien été modifié
    #     edited_message = Message.objects.get(id=message.id)
    #     self.assertEqual(edited_message.body, 'Modified Test body')
