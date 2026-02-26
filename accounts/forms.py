from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Your full name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class' : 'form-control',
            'placeholder' : 'Your email address'
        })
    )
    role = forms.ChoiceField(
        choices=User.Role.choices,
        widget=forms.Select(attrs={
            'class' : 'form-control'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone number (optional)'
        })
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'role', 'phone', 'password1', 'password2']

    def save(self, commit = True):
        # commit=False creates user in memory without saving to DB
        # allowing us to add custom fields before the final save
        user = super().save(commit=False)
        # Use email as username so users log in with email not a separate username
        user.username = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user