from django import forms
from django.forms import ModelForm
from .models import *

class MusicImageForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['audio_file','coverMusic']


class UserImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatarImg']