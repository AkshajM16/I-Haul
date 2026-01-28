from django import forms
from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    """
    Form with a single text box for writing a message in a conversation
    """
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full py-4 px-6 rounded-xl border'})
        }
