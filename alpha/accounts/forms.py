from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile
from orders.models import OrderDeliveryArea, OrderDeliveryCity
from django.utils.translation import ugettext as _


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


class UserChangeFirstnameForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя")

    class Meta:
        model = User
        fields = ('first_name', )

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not data:
            raise forms.ValidationError("Это поле не должно быть пустым!")
        return data


class ProfileChangePhoneForm(forms.ModelForm):
    phone = forms.CharField(label="Телефон")

    class Meta:
        model = Profile
        fields = ('phone',)

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if not data:
            raise forms.ValidationError("Это поле не должно быть пустым!")
        return data


class ProfileChangeAddressForm(forms.ModelForm):
    areas_list = OrderDeliveryArea.objects.all()
    cities_list = OrderDeliveryCity.objects.all()

    delivery_area = forms.ChoiceField(
        choices=[('', '-- Выберите область --')] + [(area.id, area.name) for area in areas_list],
        label="Область",
        initial='Выберите область', )
    delivery_city = forms.ChoiceField(
        choices=[('', '-- Выберите город --')] + [(city.id, city.name) for city in cities_list],
        label="Город",
        initial='Выберите город', )
    delivery_address = forms.CharField(
        label="Дополнительная информация: укажите номер и адрес отделения склада перевозчика или Ваш полный почтовый адрес (не требуется заполнять при самовывозе)",
        widget=forms.Textarea, )

    class Meta:
        model = Profile
        fields = ('delivery_address',)


class UserEmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the 
    e-mail.
    """
    error_messages = {
        'email_mismatch': _("The two email addresses fields didn't match."),
        'not_changed': _("The email address is the same as the one already defined."),
    }

    new_email1 = forms.EmailField(
        label=_("New email address"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=_("New email address confirmation"),
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserEmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user
