from django.forms import ModelForm
from django import forms
from .models import *
class NewPostForm(forms.ModelForm):
    class Meta:
        model = New_Post
        fields  = ['content']