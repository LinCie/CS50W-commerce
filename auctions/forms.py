from django import forms
from django.forms import ModelForm

from .models import Listing

class ListingForm(ModelForm):
    
    class Meta:
        model = Listing
        fields = (
            "name",
            "starting_bid",
            "image_url",
            "description"
        )
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "id": "name",
                "autocomplete": "off"
            }),
            "starting_bid": forms.NumberInput(attrs={
                "class": "form-control",
                "id": "starting_bid",
                "autocomplete": "off"
            }),
            "image_url": forms.URLInput(attrs={
                "class": "form-control",
                "id": "image_url",
                "autocomplete": "off"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "id": "description"
            })
        }
        labels = {
            "name": "Listing name",
            "starting_bid": "Starting bid",
            "image_url": "Image URL",
            "description": "Listing description"
        }
        help_texts = {
            "name": "Enter your listing name",
            "starting_bid": "Enter your starting bid! Must be more than 0",
            "image_url": "Enter your image URL",
            "description": "Enter your listing description"
        }
        