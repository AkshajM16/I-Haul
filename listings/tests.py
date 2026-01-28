from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from listings.models import Category, Listing


class CategoryTests(TestCase):
    
    def test_creates_slug_from_name(self):
        cat = Category.objects.create(name='Electronics & Gadgets')
        self.assertEqual(cat.slug, 'electronics-gadgets')
    
    def test_unique_slug_generation(self):
        cat1 = Category.objects.create(name='Books')
        cat2 = Category.objects.create(name='Books')
        self.assertNotEqual(cat1.slug, cat2.slug)


class IndexViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.category = Category.objects.create(name='Electronics')
        
    def test_hides_sold_listings(self):
        sold = Listing.objects.create(
            title='Sold', price=50, category=self.category,
            seller=self.user, is_sold=True
        )
        unsold = Listing.objects.create(
            title='Available', price=30, category=self.category, seller=self.user
        )
        
        response = self.client.get(reverse('listings:index'))
        self.assertIn(unsold, response.context['listings'])
        self.assertNotIn(sold, response.context['listings'])
    
    def test_search_filters(self):
        Listing.objects.create(
            title='Laptop', price=500, category=self.category, seller=self.user
        )
        Listing.objects.create(
            title='Mouse', price=20, category=self.category, seller=self.user
        )
        
        response = self.client.get(reverse('listings:index') + '?query=laptop')
        self.assertEqual(len(response.context['listings']), 1)
    
    def test_category_filter(self):
        cat2 = Category.objects.create(name='Books')
        electronics = Listing.objects.create(
            title='Phone', price=300, category=self.category, seller=self.user
        )
        book = Listing.objects.create(
            title='Textbook', price=50, category=cat2, seller=self.user
        )
        
        response = self.client.get(f'/listings/?category={self.category.id}')
        self.assertIn(electronics, response.context['listings'])
        self.assertNotIn(book, response.context['listings'])


class DetailViewTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.category = Category.objects.create(name='Furniture')
        self.listing = Listing.objects.create(
            title='Chair', price=75, category=self.category, seller=self.user
        )
    
    def test_shows_related_items(self):
        related = Listing.objects.create(
            title='Table', price=150, category=self.category, seller=self.user
        )
        
        response = self.client.get(reverse('listings:detail', kwargs={'pk': self.listing.pk}))
        self.assertIn(related, response.context['related_listings'])


class CreateListingTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.category = Category.objects.create(name='Electronics')
    
    def test_creates_listing(self):
        self.client.login(username='user', password='pass')
        self.client.post(reverse('listings:create'), {
            'category': self.category.id,
            'title': 'Phone',
            'description': 'New',
            'price': 400
        })
        
        listing = Listing.objects.first()
        self.assertEqual(listing.seller, self.user)


class EditListingTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.category = Category.objects.create(name='Books')
        self.listing = Listing.objects.create(
            title='Textbook', price=50, category=self.category, seller=self.user
        )
    
    def test_only_seller_can_edit(self):
        self.client.login(username='other', password='pass')
        response = self.client.get(reverse('listings:edit', kwargs={'pk': self.listing.pk}))
        self.assertEqual(response.status_code, 404)
    
    def test_updates_listing(self):
        self.client.login(username='user', password='pass')
        self.client.post(reverse('listings:edit', kwargs={'pk': self.listing.pk}), {
            'title': 'Updated',
            'price': 40,
            'is_sold': False
        })
        
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.title, 'Updated')


class DeleteListingTests(TestCase):
    
    def test_deletes_listing(self):
        user = User.objects.create_user(username='user', password='pass')
        category = Category.objects.create(name='Misc')
        listing = Listing.objects.create(
            title='Item', price=10, category=category, seller=user
        )
        
        self.client.login(username='user', password='pass')
        self.client.get(reverse('listings:delete', kwargs={'pk': listing.pk}))
        
        self.assertEqual(Listing.objects.count(), 0)