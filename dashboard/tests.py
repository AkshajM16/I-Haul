from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from listings.models import Listing


class DashboardTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.url = reverse('dashboard:index')

    def test_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_shows_user_listings(self):
        other_user = User.objects.create_user(username='other', password='pass')
        
        my_listing = Listing.objects.create(
            title='My Item', description='Test', price=50, seller=self.user
        )
        other_listing = Listing.objects.create(
            title='Other', description='Test', price=30, seller=other_user
        )

        self.client.login(username='user', password='pass')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(my_listing, response.context['listings'])
        self.assertNotIn(other_listing, response.context['listings'])