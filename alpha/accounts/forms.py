from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """Form for loggin in"""
    user_email = forms.EmailField(
        required=True)
    user_password = forms.CharField(
        required=True)


class UserRegistrationForm(forms.Form):
    """Form for creating new account/registration"""
    new_user_email = forms.EmailField(
        required=True,
        max_length=240)
    new_user_name = forms.CharField(
        required=True,
        max_length=240)
    password = forms.CharField(
        required=True)
    password_repeat = forms.CharField(
        required=True)

    class Meta:
        model = User

    def clean_username(self):
        username = self.cleaned_data['new_user_email']

    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_repeat']:
            raise forms.ValidationError('Введенные пароли не совпадают')
        return cd['password_repeat']


class UserAddPersonalForm(forms.Form):
    """Form for User name or phone adding or editing"""
    user_firstname = forms.CharField()
    profile_phone = forms.CharField()
