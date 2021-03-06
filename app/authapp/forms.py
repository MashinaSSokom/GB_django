import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from authapp.models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):

    class Meta:
        model = ShopUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):

    class Meta:
        model = ShopUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'avatar', 'age']

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise forms.ValidationError('Вы слишком молоды')

        return age

    def save(self, commit=True):
        user = super(ShopUserRegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserEditForm(UserChangeForm):

    class Meta:
        model = ShopUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'avatar', 'age']

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.__class__ == forms.fields.BooleanField:
                field.widget.attrs['class'] = 'form-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise forms.ValidationError('Вы слишком молоды')
        return age


class ShopUserProfileEditForm(forms.ModelForm):

    class Meta:
        model = ShopUserProfile
        fields = ['url', 'tagline', 'about_me', 'gender']

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
