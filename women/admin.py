from django.contrib import admin

# Нужно импортировать модель для регистрации её в панели админа
# В данном случае импортируем все
from .models import *


# Вспомогательный класс. Women - от названия модели, для которой описывается вспомогательный класс,
# Admin - говорит о том, что он будет использоваться для панели админа.
# Также нужно зарегистрировать класс admin.site.register.
class WomenAdmin(admin.ModelAdmin):

    # Названия берутся по атрибутам модели Women.

    # Содержит список полей, которые мы хотим видеть в таблице Women админ панели.
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')

    # Содержит поля, на которые можно кликнуть и перейтина соответствующую статью (для редактирования).
    list_display_links = ('id', 'title')

    # Говорит по каким полям можно производить поиск информации.
    search_fields = ('title', 'content')

    # Список полей, которые будут открыты для редактирования непосредственно в списке (таблице) Women.
    list_editable = ('is_published',)

    # Список полей, по которым можно фильтровать список.
    list_filter = ('is_published', 'time_create')

    # При помощи этого атрибута указывается, что поле slug
    # должно автоматически заполняться на основе поля name.
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

    # Нужно обязательно ставить запятую при одном параметре,
    # так как передать нужно кортеж.
    search_fields = ('name',)

    # При помощи этого атрибута указывается, что поле slug
    # должно автоматически заполняться на основе поля name.
    prepopulated_fields = {'slug': ('name',)}


# Регистрация модели Women в админ панели.
# Благодаря функции модели Women get_absolute_url
# админ панель добавила кнопку "Смотреть на сайте".
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
