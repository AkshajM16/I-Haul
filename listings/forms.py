from django import forms
from .models import Listing

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewListingForm(forms.ModelForm):
    """
    Form used when creating a new listing.
    """
    class Meta:
        model = Listing
        fields = ('category', 'title', 'description', 'price', 'image')
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'title': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'What are you selling?'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES})
        }

class EditListingForm(forms.ModelForm):
    """
    Form used when editing an existing listing.
    """
    class Meta:
        model = Listing
        fields = ('title', 'description', 'price', 'image', 'is_sold')
        widgets = {
            'title': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES})
        }