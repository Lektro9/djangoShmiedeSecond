from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Thema, Karten
from tinymce.widgets import TinyMCE

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CreateThemaForm(forms.ModelForm):
    class Meta:
        model = Thema
        fields = ["thema_fach", "name", "inhalt"]
        widgets = {'inhalt': TinyMCE()}

class CreateKartenForm(forms.ModelForm):
    class Meta:
        model = Karten
        fields = ["karten_thema", "frage", "antwort"]