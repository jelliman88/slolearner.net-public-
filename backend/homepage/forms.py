from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from django import forms
from django.forms import CharField, EmailField, EmailInput, ModelChoiceField, PasswordInput, TextInput
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext


class NewUserForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username']
        
    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = EmailInput(attrs={'class': 'form-control', 'placeholder':  _('email')})
        self.fields['username'].widget = TextInput(attrs={'class': 'form-control', 'placeholder':  _('username')})
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder':  _('password')})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder':  _('repeat password')})
        for fieldname in ['email','username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ''

class UserAuthenticationForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'class': 'form-control', 'placeholder':  _('email')})
        self.fields['password'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': _('password')})
        for fieldname in ['username','password']:
            self.fields[fieldname].label = ''
            


    def confirm_login_allowed(self, user):
        
        if not user.is_active or not user.is_validated:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')
