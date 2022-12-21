from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}]


# Класс мексин для устранения дублирования в классах представлений.
class DataMixin:

    # Для реализации пагинации дочернего класса.
    paginate_by = 3

    # Этот метод создает контекст для шаблона.
    def get_user_context(self, **kwargs):


        # Формируется начальный словарь из переданных именнованных параметров.
        context = kwargs

        # Реализация кэширования на уровне API.
        # Берем из кэша коллекцию по ключу cats.
        cats = cache.get('cats')

        # Если коллекция пустая (в кэше ничего нет по ключу cats).
        if not cats:
            # Формируется список категорий и добавляем к каждому объекту количество связанных статей.
            cats = Category.objects.annotate(Count('women'))

            # Коллекция сохраняется в кэше по ключу cats.
            cache.set('cats', cats, 60)

        # Копируем меню.
        user_menu = menu.copy()

        # Проверяем авторизацию через объект request экземпляра класса DataMixin (self).
        # Миксин связан с запросом, а у запроса есть объект request. У объекта request есть объект user,
        # у user есть свойство is_authenticated. Если is_authenticated == true - значит авторизован.
        if not self.request.user.is_authenticated:

            # Если пользователь не авторизован, то из user_menu удаляем 1 элемент (по индекску).
            user_menu.pop(1)

        # Добавляем в контекст меню.
        context['menu'] = user_menu

        # Добавляем в контекст категории.
        context['cats'] = cats

        # Проверяем наличие параметра cat_selected в контексте, если его нет - добавляем.
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context
