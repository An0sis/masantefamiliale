from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('user','email','phone','address')  # replace with your actual fields

class CombinedForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField()
        self.fields['phone'] = forms.CharField()
        self.fields['address'] = forms.CharField()

    def is_valid(self):
        return super().is_valid()

    def save(self, commit=True):
        user = super().save(commit)
        client, created = Client.objects.get_or_create(
            user=user,
            defaults={
                'email': self.cleaned_data['email'],
                'phone': self.cleaned_data['phone'],
                'address': self.cleaned_data['address']
            }
        )
        if not created:
            client.email = self.cleaned_data['email']
            client.phone = self.cleaned_data['phone']
            client.address = self.cleaned_data['address']
        if commit:
            client.save()
        return user

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'username'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'password'}))