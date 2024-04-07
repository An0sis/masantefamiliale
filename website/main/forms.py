from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, Disease


class ClientForm(forms.ModelForm):
    diseases = forms.ModelMultipleChoiceField(
        queryset=Disease.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Client
        fields = (
            'user', 'email', 'phone', 'name', 'lastname', 'birthdate', 'father_name', 'mother_name', 'brother_sister',
            'gender', 'diseases')  # replace with your actual fields


class CombinedForm(UserCreationForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['email'] = forms.EmailField(required=False)
        self.fields['phone'] = forms.CharField(required=False)
        self.fields['name'] = forms.CharField()
        self.fields['lastname'] = forms.CharField()
        self.fields['birthdate'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        self.fields['father_name'] = forms.CharField(required=False)
        self.fields['mother_name'] = forms.CharField(required=False)
        self.fields['brother_sister'] = forms.CharField(required=False)
        self.fields['gender'] = forms.BooleanField()
        self.fields['diseases'] = forms.ModelMultipleChoiceField(
            queryset=Disease.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False
        )

    def is_valid(self):
        return super().is_valid()

    def clean_diseases(self):
        diseases = self.cleaned_data['diseases']
        if not diseases:
            diseases = []
        return diseases

    def save(self, commit=True):
        user = super().save(commit)
        client, created = Client.objects.get_or_create(
            user=user,
            defaults={
                'email': self.cleaned_data['email'],
                'phone': self.cleaned_data['phone'],
                'name': self.cleaned_data['name'],
                'lastname': self.cleaned_data['lastname'],
                'birthdate': self.cleaned_data['birthdate'],
                'father_name': self.cleaned_data['father_name'],
                'mother_name': self.cleaned_data['mother_name'],
                'brother_sister': self.cleaned_data['brother_sister'],
                'gender': self.cleaned_data['gender']
            }
        )
        if not created:
            client.email = self.cleaned_data['email']
            client.phone = self.cleaned_data['phone']
            client.name = self.cleaned_data['name']
            client.lastname = self.cleaned_data['lastname']
            client.birthdate = self.cleaned_data['birthdate']
            client.father_name = self.cleaned_data['father_name']
            client.mother_name = self.cleaned_data['mother_name']
            client.brother_sister = self.cleaned_data['brother_sister']
            client.gender = self.cleaned_data['gender']

        diseases = self.cleaned_data.get('diseases', [])
        client.diseases.set(diseases)

        if commit:
            client.save()
        return user


from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'username'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'password'}))
