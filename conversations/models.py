from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from listings.models import Listing


class Conversation(models.Model):
    """
    A conversation thread about a listing
    """
    listing = models.ForeignKey(Listing, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    # Updated whenever a new message is posted
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Most recent conversation shown first
        ordering = ('-modified_at',)

    def __str__(self):
        member_names = ", ".join(self.members.values_list('username', flat=True)[:3])
        return f"Conversation on '{self.listing.title}' with [{member_names}]"


class ConversationMessage(models.Model):
    """
    A message within the conversation thread opened.
    """
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='conversation_messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message by {self.created_by.username} @ {self.created_at:%Y-%m-%d %H:%M}"
    
# When a message is created, 'touch' the parent conversation so it floats to the top of the inbox
@receiver(post_save, sender=ConversationMessage)
def touch_conversation_modified_at(sender, instance, created, **kwargs):
    if created:
        instance.conversation.save(update_fields=['modified_at'])