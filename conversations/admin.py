from django.contrib import admin
from .models import Conversation, ConversationMessage


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'modified_at')
    list_filter = ('modified_at', 'created_at')
    search_fields = ('listing__title', 'members__username')
    filter_horizontal = ('members',)


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'created_by__username')