# slmsapp/forms.py

from django import forms
from .models import UserFeedback, AdminFeedback
from slmsapp.models import CustomUser  # Import your CustomUser model
from django.contrib.auth import get_user_model



class UserFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class AdminFeedbackForm(forms.ModelForm):
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.fields['employee'].queryset = get_user_model().objects.all()

    class Meta:
        model = AdminFeedback
        fields = ['employee', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }