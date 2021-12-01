from django import forms
from .models import*
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,UserChangeForm

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'validate'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'validate'}))
    class Meta:
        model = User
        fields = ['email','first_name','last_name']
        labels = {'email':'Email','first_name':'First Name','last_name':'Last Name'}
        widgets = {k:forms.TextInput(attrs={'placeholder':v,'class':'validate'}) for k,v in labels.items()}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'placeholder':'Email','class':'validate'}))
    password = forms.CharField(label=_("Password"),strip=False,
            widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'validate'}))

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Password"),strip=False,
            widget=forms.PasswordInput(attrs={'placeholder':'Old Password','class':'validate'}))
    new_password1 = forms.CharField(label=_("Password"),strip=False,
            widget=forms.PasswordInput(attrs={'placeholder':'New Password','class':'validate'}))
    new_password2 = forms.CharField(label=_("Password"),strip=False,
            widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'validate'}))
            
class ChangeUserProfileForm(UserChangeForm):
    password = forms.PasswordInput()
    class Meta:
        model = User
        fields = {'first_name','last_name','password'}
        labels = {'first_name':'First Name','last_name':'Last Name'}
        widgets = {
            'first_name':forms.TextInput(attrs={'placeholder':'First Name','class':'validate'}),
            'last_name':forms.TextInput(attrs={'placeholder':'Last Name','class':'validate'}),
        }
