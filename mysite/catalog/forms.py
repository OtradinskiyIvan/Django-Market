from django import forms
from .models import *


class AddItemForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255, label='URL')
    seller_id = forms.IntegerField()
    price = forms.IntegerField()
    desc = forms.CharField(widget=forms.Textarea())
    is_available = forms.BooleanField(initial=True, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Set category')
    tags = forms.ModelChoiceField(queryset=Tag.objects.all(), empty_label='Set tag')


class ContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea())
    