from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from listings.models import Listing, Category


class IndexViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('main:index')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@illinois.edu',
            password='testpass123'
        )

    def test_index_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_shows_categories(self):
        category = Category.objects.create(name='Electronics')
        response = self.client.get(self.url)
        self.assertIn('categories', response.context)
        self.assertIn(category, response.context['categories'])

    def test_newest_listings_shown(self):
        listing = Listing.objects.create(
            title='Test Item',
            description='Test description',
            price=50,
            seller=self.user
        )
        response = self.client.get(self.url)
        self.assertIn('listings', response.context)
        self.assertIn(listing, response.context['listings'])

    def test_sell_button_when_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertContains(response, 'Sell an Item')


class LoginViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('main:login')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_works(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('main:index'))

    def test_wrong_password(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')


class SignupViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('main:signup')

    def test_signup_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'new@illinois.edu',
            'password1': 'securepass123',
            'password2': 'securepass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_passwords_dont_match(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'new@illinois.edu',
            'password1': 'securepass123',
            'password2': 'differentpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_username_already_exists(self):
        User.objects.create_user(username='existing', password='pass')
        response = self.client.post(self.url, {
            'username': 'existing',
            'email': 'new@illinois.edu',
            'password1': 'securepass123',
            'password2': 'securepass123'
        })
        self.assertEqual(response.status_code, 200)