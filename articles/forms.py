from django import forms
from django.forms import Textarea
from . import models

class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ["title", "body", "slug", "thumb"]

class AddComment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['message']
        labels = {
            'message': 'Comment',
        }
