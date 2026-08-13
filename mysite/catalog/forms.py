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
    images = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'multiple': True})
    )
    video = forms.FileField(required=False)

    MAX_IMAGES = 4
    MAX_VIDEO_MB = 250
    ALLOWED_VIDEO_EXTS = ('mp4', 'webm')

    def clean(self):
        clean_data = super().clean()
        images = self.files.getlist('images')

        if len(images) > self.MAX_IMAGES:
            self.add_error(None, (f'You can upload only {self.MAX_IMAGES} images'))


        video = self.files.get('video')
        if video:
            if video.size > self.MAX_VIDEO_MB * 1024 * 1024:
                self.add_error(None, f'Video can be only {self.MAX_VIDEO_MB} MB max.')
            name = video.name
            ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''
            if ext not in self.ALLOWED_VIDEO_EXTS:
                self.add_error(None, 'Video must have mp4 or webm format.')

        return clean_data



class ContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea())
    