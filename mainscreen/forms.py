from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': ' form-control'}))

    class Meta:
        model = User
        fields = ('email',)


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'type': 'email',
        'style': 'height:40px',
        'placeholder': 'example@edu.hse.ru'
    }))