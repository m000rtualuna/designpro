from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Пароль (повторно)", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'username', 'email', 'password', 'password_confirm', 'agreement')
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'patronymic': 'Отчество', 'username': 'Логин', 'email': 'Почта', 'agreement': 'Я согласен на обработку персональных данных'}

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            pattern = r"^[а-яА-Я -]+$"
            if not re.fullmatch(pattern, first_name):
                raise forms.ValidationError("Имя должно содержать только кириллические буквы, дефисы и пробелы")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            pattern = r"^[а-яА-Я -]+$"
            if not re.fullmatch(pattern, last_name):
                raise forms.ValidationError("Фамилия должна содержать только кириллические буквы, дефисы и пробелы")
        return last_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        if patronymic:
            pattern = r"^[а-яА-Я -]+$"
            if not re.fullmatch(pattern, patronymic):
                raise forms.ValidationError("Отчество должно содержать только кириллические буквы, дефисы и пробелы")
        return patronymic

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            errors = {'password_confirm': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

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