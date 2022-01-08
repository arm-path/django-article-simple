import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import ValidationError

from captcha.fields import CaptchaField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Article, Category, Section, Subject


class SectionForm(forms.ModelForm):
    """ Форма создания и редактирования разделов """

    class Meta:
        model = Section
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form_input_shadow'}),
        }

    def clean_title(self):
        """ Валидация поля title """
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должено начинаться с цифры')
        return title


class CategoryForm(forms.ModelForm):
    """ Форма создания и редактирования категорий """

    class Meta:
        model = Category
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form_input_shadow'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должено начинаться с цифры')
        return title


class SubjectForm(forms.ModelForm):
    """ Форма создания и редактирования тем """

    class Meta:
        model = Subject
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form_input_shadow'}),
        }

    def clean_title(self):
        """ Валидация поля title """
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должено начинаться с цифры')
        return title


class ArticleForm(forms.ModelForm):
    """ Форма создания и редактирования статей """

    class Meta:
        model = Article
        fields = ['title', 'section', 'category', 'subject', 'content_description', 'content', 'image_publication']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form_input_shadow'}),
            'category': forms.Select(attrs={'class': 'form-control form_input_shadow'}),
            'section': forms.Select(attrs={'class': 'form-control form_input_shadow'}),
            'subject': forms.Select(attrs={'class': 'form-control form_input_shadow'}),
            'content_description': forms.Textarea(attrs={'class': 'form-control form_input_shadow', 'rows': 3}),
            'content': CKEditorUploadingWidget(attrs={'class': 'form-control form_input_shadow', 'rows': 6}),
        }

    def clean_title(self):
        """ Валидация поля title """
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должено начинаться с цифры')
        return title


class UserRegistration(UserCreationForm):
    """ Форма регистрации пользователя """
    username = forms.CharField(max_length=150, label='Имя пользователя',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control form_input_shadow', 'autocomplete': None}))
    email = forms.EmailField(max_length=150, label="Электронная почта",
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control form_input_shadow', 'autocomplete': None}))
    password1 = forms.CharField(max_length=150, label='Пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control form_input_shadow', 'autocomplete': None}))
    password2 = forms.CharField(max_length=150, label='Подтверждение пароля',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control form_input_shadow', 'autocomplete': None}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserAuthorization(AuthenticationForm):
    """ Форма авторизации пользователя """
    username = forms.CharField(max_length=150, label="Имя пользователя", widget=forms.TextInput(
        attrs={'class': 'form-control form_input_shadow', 'autocomplete': None}))
    password = forms.CharField(max_length=150, label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control form_input_shadow', 'autocomplete': None}))


class Feedback(forms.Form):
    """ Форма обратной связи """
    title = forms.CharField(max_length=150, label='Заголовок', widget=forms.TextInput(
        attrs={'class': 'form-control form_input_shadow', 'autocomplete': None}))
    content = forms.CharField(max_length=150, label='Текст письма', widget=forms.Textarea(
        attrs={'class': 'form-control form_input_shadow'}))
    captcha = CaptchaField(label='Введите текст с картинки: ')
