from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

from posts.models import UserRequest

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Пароль (повторно)", widget=forms.PasswordInput)
    username = forms.CharField(label="Логин", help_text='')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'username', 'email', 'password', 'password_confirm', 'agreement')
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'patronymic': 'Отчество', 'email': 'Почта', 'agreement': 'Я согласен на обработку персональных данных'}

        error_messages = {
            'username': {
                'unique': "Пользователь с таким логином уже зарегистрирован",
            },
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not re.fullmatch(r"^[а-яА-Я -]+$", first_name):
            raise forms.ValidationError("Имя должно содержать только кириллицу, дефисы и пробелы")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not re.fullmatch(r"^[а-яА-Я -]+$", last_name):
            raise forms.ValidationError("Фамилия должна содержать только кириллицу, дефисы и пробелы")
        return last_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        if patronymic and not re.fullmatch(r"^[а-яА-Я -]+$", patronymic):
            raise forms.ValidationError("Отчество должно содержать только кириллицу, дефисы и пробелы")
        return patronymic

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and not re.fullmatch(r"^[a-zA-z-]+$", username):
            raise forms.ValidationError("Логин должен содержать только латиницу и дефисы")
        return username

    def clean(self):
        super().clean()
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            raise ValidationError({'password_confirm': 'Введенные пароли не совпадают'})
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_agreement(self):
        agreement = self.cleaned_data.get('agreement')
        if not agreement:
            raise forms.ValidationError('Вы должны согласиться на обработку персональных данных')
        return agreement

class RequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ['title', 'description', 'image']