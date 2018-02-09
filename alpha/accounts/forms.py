from django import forms


class LoginForm(forms.Form):
	"""Форма для входа в систему"""
	user_email = forms.EmailField(
		required=True
		)
	user_password = forms.CharField(
		required=True
		)
