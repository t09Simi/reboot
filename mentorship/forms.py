from django import forms
from .models import Session

class SessionForm(forms.ModelForm):

    DURATION_CHOICES = [
    (30, '30 minutes'),
    (45, '45 minutes'),
    (60, '1 hour'),
    (90, '1.5 hours'),
    (120, '2 hours'), ]

    scheduled_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class' : 'form-control',
             'type': 'datetime-local'
        })
    )

    duration = forms.ChoiceField(
    choices=DURATION_CHOICES,
    widget=forms.Select(attrs={
        'class': 'form-control'
    })
    )

    meeting_link = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://meet.google.com/your-link'
        })
    )

    class Meta:
        model = Session
        fields = ['scheduled_at', 'duration', 'meeting_link']
