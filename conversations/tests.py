from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from listings.models import Listing
from conversations.models import Conversation, ConversationMessage


class ConversationModelTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.listing = Listing.objects.create(
            title='Item', description='Test', price=50, seller=self.user
        )
        
    def test_message_updates_conversation_timestamp(self):
        convo = Conversation.objects.create(listing=self.listing)
        old_modified = convo.modified_at
        
        ConversationMessage.objects.create(
            conversation=convo, content='Hi', created_by=self.user
        )
        
        convo.refresh_from_db()
        self.assertGreater(convo.modified_at, old_modified)


class NewConversationTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.seller = User.objects.create_user(username='seller', password='pass')
        self.buyer = User.objects.create_user(username='buyer', password='pass')
        self.listing = Listing.objects.create(
            title='Item', description='Test', price=50, seller=self.seller
        )
        
    def test_seller_cannot_message_self(self):
        self.client.login(username='seller', password='pass')
        response = self.client.get(
            reverse('conversations:new', kwargs={'listing_pk': self.listing.pk})
        )
        self.assertRedirects(response, reverse('listings:detail', kwargs={'pk': self.listing.pk}))
        
    def test_creates_conversation_with_message(self):
        self.client.login(username='buyer', password='pass')
        self.client.post(
            reverse('conversations:new', kwargs={'listing_pk': self.listing.pk}),
            {'content': 'Hello'}
        )
        
        convo = Conversation.objects.first()
        self.assertEqual(convo.members.count(), 2)
        self.assertEqual(convo.messages.count(), 1)
        
    def test_reuses_existing_conversation(self):
        convo = Conversation.objects.create(listing=self.listing)
        convo.members.add(self.buyer, self.seller)
        
        self.client.login(username='buyer', password='pass')
        response = self.client.get(
            reverse('conversations:new', kwargs={'listing_pk': self.listing.pk})
        )
        
        self.assertRedirects(response, reverse('conversations:detail', kwargs={'pk': convo.pk}))


class InboxTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.listing = Listing.objects.create(
            title='Item', description='Test', price=50, seller=self.user1
        )
        
    def test_shows_only_user_conversations(self):
        convo1 = Conversation.objects.create(listing=self.listing)
        convo1.members.add(self.user1)
        
        convo2 = Conversation.objects.create(listing=self.listing)
        convo2.members.add(self.user2)
        
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('conversations:inbox'))
        
        self.assertIn(convo1, response.context['conversations'])
        self.assertNotIn(convo2, response.context['conversations'])


class ConversationDetailTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.listing = Listing.objects.create(
            title='Item', description='Test', price=50, seller=self.user
        )
        self.convo = Conversation.objects.create(listing=self.listing)
        self.convo.members.add(self.user)
        
    def test_posts_message(self):
        self.client.login(username='user', password='pass')
        self.client.post(
            reverse('conversations:detail', kwargs={'pk': self.convo.pk}),
            {'content': 'New message'}
        )
        
        msg = self.convo.messages.first()
        self.assertEqual(msg.content, 'New message')
        self.assertEqual(msg.created_by, self.user)