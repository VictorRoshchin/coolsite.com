from django import template
from women.models import *


# Создаем экземпляр класса Library, через который будет происходить
# регистрация собственных шаблонных тегов.
register = template.Library()


# Функия для работы простого тега.
# При помощи декоратора simple_tag превращаем функцию в тег
# (декоратор доступен через экземпляр register класса Library).
# Параметр name - меняет отображаемое имя декоратора в шаблоне.
@register.simple_tag(name='getcats')
def get_categories(filter=None):

    # Функция просто возвращает выбранные категории из БД.
    # Если фильтра нет, то возвращается весь список.
    if not filter:
        return Category.objects.all()

    # Иначе будет выполнена функция filter.
    else:
        return Category.objects.filter(pk=filter)

# Включающий тег, позволяет дополнительно формировать свой собственный
# шаблон на основе некоторых данных и возвращать фрагмент HTML-страницы.
# Возвращаемые параметр будет автоматически передаваться в выбранный шаблон,
# который будет фрагментом другого html-файла.
# Фрагмент будет возвращаться самим тегом в базовый шаблон.
@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):

    # Если сортировка не определена, то возвращается весь список.
    if not sort:
        cats = Category.objects.all()

    # Иначе вызывается функция order_by (сортировка по указанному полю).
    else:
        cats = Category.objects.order_by(sort)

    # Параметр cat_selected передается шаблону (фрагменту),
    # чтобы проверить какая рубрика выбрана и отобразить
    # её как обычный текст.
    return {"cats": cats, "cat_selected": cat_selected}


@register.simple_tag(name='getmenu')
def get_menu():
    menu = [{'title': "О сайте", 'url_name': 'about'},
            {'title': "Добавить статью", 'url_name': 'add_page'},
            {'title': "Обратная связь", 'url_name': 'contact'},
            {'title': "Войти", 'url_name': 'login'}]
    return menu
