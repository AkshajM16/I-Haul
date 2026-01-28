from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from listings.models import Listing


class ProfileViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@illinois.edu',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.url = reverse('account:profile')

    def test_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_shows_profile(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_obj'], self.user)

    def test_shows_only_user_listings(self):
        other_user = User.objects.create_user(username='other', password='pass')
        my_listing = Listing.objects.create(
            title='My Item', description='Test', price=50, seller=self.user
        )
        other_listing = Listing.objects.create(
            title='Other', description='Test', price=30, seller=other_user
        )

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        
        self.assertIn(my_listing, response.context['listings'])
        self.assertNotIn(other_listing, response.context['listings'])


class EditProfileViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@illinois.edu',
            password='testpass123'
        )
        self.url = reverse('account:edit')

    def test_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_shows_form(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_updates_profile(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'new@illinois.edu'
        })
        
        self.assertRedirects(response, reverse('account:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'new@illinois.edu')

    def test_invalid_email(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid'
        })
        
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@illinois.edu')


class ProfileFormTests(TestCase):
    
    def test_valid_form(self):
        from account.forms import ProfileForm
        user = User.objects.create_user(username='test', password='pass')
        form = ProfileForm(
            data={'first_name': 'Test', 'last_name': 'User', 'email': 'test@test.com'},
            instance=user
        )
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        from account.forms import ProfileForm
        user = User.objects.create_user(username='test', password='pass')
        form = ProfileForm(
            data={'first_name': 'Test', 'last_name': 'User', 'email': 'bad-email'},
            instance=user
        )
        self.assertFalse(form.is_valid())


class PasswordChangeTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='oldpass')
        self.url = reverse('account:password')

    def test_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_changes_password(self):
        self.client.login(username='test', password='oldpass')
        response = self.client.post(self.url, {
            'old_password': 'oldpass',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123'
        })
        
        self.assertRedirects(response, '/account/')
        self.client.logout()
        self.assertTrue(self.client.login(username='test', password='newpass123'))


class URLTests(TestCase):
    
    def test_urls_resolve(self):
        self.assertEqual(reverse('account:profile'), '/account/')
        self.assertEqual(reverse('account:edit'), '/account/edit/')
        self.assertEqual(reverse('account:logout'), '/account/logout/')
        self.assertEqual(reverse('account:password'), '/account/password/')