from django import forms
from .models import BlogPost, Picture
from django.forms import inlineformset_factory


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'discription']


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image']


# forms.py
PictureFormSet = inlineformset_factory(BlogPost, Picture, form=PictureForm, extra=3, can_delete=True)
