from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CareerGapProfile, MentorProfile

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
    
class CareerGapProfileForm(forms.ModelForm):

    employment_status = forms.ChoiceField(
        choices=CareerGapProfile.EmploymentStatus.choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    education = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your education details'
        })
    )
    prior_experience = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Share your work experience details if any'
        })
    )
    certifications = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Certifications if any'
        })
    )
    projects = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Projects if any'
        })
    )
    portfolio = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://yourportfolio.com'
        })
    )
    interests = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Web Development, Data Analysis'
        })
    )
    gap_story = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Tell us your story...'
        })
    )
    gap_duration = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of years'
        })
    )

    class Meta:
        model = CareerGapProfile
        fields = [
            'employment_status',
            'education',
            'prior_experience',
            'certifications',
            'projects',
            'portfolio',
            'interests',
            'gap_story',
            'gap_duration'
        ]

class MentorProfileForm(forms.ModelForm):

    education = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your education details'
        })
    )
    skills = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Skills you have'
        })
    )
    company = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your current company'
        })
    )
    years_of_experience = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    portfolio = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://yourportfolio.com'
        })
    )
    interests = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Web Development, Data Analysis'
        })
    )
    availability = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )
    availability_times = forms.CharField(
        required= False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Weekends 10am-12pm IST'
        })
    )
    class Meta:
        model = MentorProfile
        fields = [
            'education',
            'skills',
            'company',
            'years_of_experience',
            'portfolio',
            'interests',
            'availability',
            'availability_times'
        ]