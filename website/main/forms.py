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
            'user', 'email', 'phone', 'name', 'lastname', 'age', 'father_name', 'mother_name', 'brother_sister',
            'diseases')  # replace with your actual fields


class CombinedForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField()
        self.fields['phone'] = forms.CharField()
        self.fields['name'] = forms.CharField()
        self.fields['lastname'] = forms.CharField()
        self.fields['age'] = forms.IntegerField()
        self.fields['father_name'] = forms.CharField()
        self.fields['mother_name'] = forms.CharField()
        self.fields['brother_sister'] = forms.CharField()
        self.fields['diseases'] = forms.ModelMultipleChoiceField(
            queryset=Disease.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False
        )

    def is_valid(self):
        return super().is_valid()

    def save(self, commit=True):
        user = super().save(commit)
        client, created = Client.objects.get_or_create(
            user=user,
            defaults={
                'email': self.cleaned_data['email'],
                'phone': self.cleaned_data['phone'],
                'name': self.cleaned_data['name'],
                'lastname': self.cleaned_data['lastname'],
                'age': self.cleaned_data['age'],
                'father_name': self.cleaned_data['father_name'],
                'mother_name': self.cleaned_data['mother_name'],
                'brother_sister': self.cleaned_data['brother_sister'],
            }
        )
        if not created:
            client.email = self.cleaned_data['email']
            client.phone = self.cleaned_data['phone']
            client.name = self.cleaned_data['name']
            client.lastname = self.cleaned_data['lastname']
            client.age = self.cleaned_data['age']
            client.father_name = self.cleaned_data['father_name']
            client.mother_name = self.cleaned_data['mother_name']
            client.brother_sister = self.cleaned_data['brother_sister']

        diseases = self.cleaned_data['diseases']
        for disease in diseases:
            client.diseases.add(disease)

        if commit:
            client.save()
        return user