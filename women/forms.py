from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


# Название класса придумываем сами, наследуется от базового класса forms.ModelForm.
class AddPostForm(forms.ModelForm):

    # Конструктор, который вызывает super (с конструктором базового класса),
    # а затем поле cat модифицируется.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    # Вложенный класс мета.
    class Meta:

        # Создает связь с моделью Women.
        model = Women

        # Говорит, какие поля нужно отобразить в форме.
        # __all__ - все поля, кроме тех, что заполняются автоматически.
        # Лучше явно указывать все нужные поля.
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']

        # Атрибут для определения стилей.
        widgets = {

            # Определения стиля для поля с заголовков.
            'title': forms.TextInput(attrs={'class': 'form-input'}),

            # Определения стиля для поля с текстом статьи.
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # Метод пользовательского валидатора.
    # Название метода должно быть "clean_<название поля>".
    # Этот метод должен генерировать исключение ValidationError.
    def clean_title(self):

        # Создаем переменную (ссылку на данные из поля title).
        title = self.cleaned_data['title']

        # Проверяем требуемое условия.
        if len(title) > 200:

            # Если оно нарушается, генерируем исключение с текстом.
            raise ValidationError('Длина превышает 200 символов')

        # Возвращаем вадидное значение.
        return title


## Название класса придумываем сами, наследуется от базового класса forms.Form.
# # Атрибуты класса - это поля формы. Форма будет связана с БД,
# # поэтому лучше называть её атрибуты также, как и у связанной таблицы.
# # Параметр label - название поля в форме.
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label="URL")
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
#
#     # required=False - поле является необязательным.
#     # initial=True - по умолчанию чекбокс будет отмеченным.
#     is_published = forms.BooleanField(label="Публикация", required=False, initial=True)
#
#     # Поле ModelChoiceField будет выпадающим списком и формируется на основе класса Category.
#     # empty_label -значение при невыбранной категории (вместо дефисов).
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории", empty_label="Категория не выбрана")


# Пользовательская форма регистрации создается на базе класса UserCreationForm.
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:

        # Указываем с какой моделью (таблицей БД) связываем форму.
        model = User

        # Поля, которые будут отображаться.
        # Названия полей можно посмотреть через дефтулс браузера
        # (атрибут name у соответствующего инпута).
        fields = ('username', 'email', 'password1', 'password2')


# Пользовательский класс авторизации.
class LoginUserForm(AuthenticationForm):

    # В форме авторизации не нужно указывать класс Meta,
    # как в форме регистрации, достаочно указать только эти два атрибутп (поля),
    # или еще какие-либо дополнительные, если требуется.
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='Введите символы')
