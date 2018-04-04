from django import forms
from .models import OrderDeliveryArea, OrderDeliveryCity
from django.contrib.auth.models import User
from accounts.models import Profile


class UserCheckoutForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя")
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ('first_name', 'email', )

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not data:
            raise forms.ValidationError("Это поле не должно быть пустым!")
        return data


class ProfileCheckoutForm(forms.ModelForm):
    areas_list = OrderDeliveryArea.objects.all()
    cities_list = OrderDeliveryCity.objects.all()

    phone = forms.CharField(label="Телефон")
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
        fields = ('phone', 'delivery_area', 'delivery_city', 'delivery_address', )

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if not data:
            raise forms.ValidationError("Это поле не должно быть пустым!")
        return data


class AnonymousCheckoutForm(forms.Form):
    areas_list = OrderDeliveryArea.objects.all()
    cities_list = OrderDeliveryCity.objects.all()

    anonymous_name = forms.CharField(
        required=True,
        label='Имя',
    )
    anonymous_email = forms.EmailField(
        required=True,
        label='Email',
    )
    anonymous_phone = forms.CharField(
        required=True,
        label='Телефон',
    )
    anonymous_area = forms.ChoiceField(
        choices=[('', '-- Выберите область --')] + [(area.id, area.name) for area in areas_list],
        label="Область",
        initial='Выберите область', )
    anonymous_city = forms.ChoiceField(
        choices=[('', '-- Выберите город --')] + [(city.id, city.name) for city in cities_list],
        label="Город",
        initial='Выберите город', )
    anonymous_additional = forms.CharField(
        label="Дополнительная информация: укажите номер и адрес отделения склада перевозчика или Ваш полный почтовый адрес (не требуется заполнять при самовывозе)",
        widget=forms.Textarea, )

    def clean_anonymous_name(self):
        data = self.cleaned_data['anonymous_name']
        if not data:
            raise forms.ValidationError("Это поле не должно быть пустым!")
        return data

    def clean_anonymous_email(self):
        data = self.cleaned_data['anonymous_email']
        if not data:
            raise forms.ValidationError("Это поле не должно быть пустым!")
        return data

    def clean_anonymous_phone(self):
        data = self.cleaned_data['anonymous_phone']
        if not data:
            raise forms.ValidationError("Это поле не должно быть пустым!")
        return data
