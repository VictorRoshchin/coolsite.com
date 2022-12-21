from django.contrib import admin
from django.utils.safestring import mark_safe

# Нужно импортировать модель для регистрации её в панели админа
# В данном случае импортируем все
from .models import *


# Вспомогательный класс. Women - от названия модели, для которой описывается вспомогательный класс,
# Admin - говорит о том, что он будет использоваться для панели админа.
# Также нужно зарегистрировать класс admin.site.register.
class WomenAdmin(admin.ModelAdmin):

    # Названия берутся по атрибутам модели Women.

    # Содержит список полей, которые мы хотим видеть в таблице Women админ панели.
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')

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

    # Этот атрибут содержит список и порядок редактируемых полей конкретной записи.
    # Нередактируемые по умолчанию добавлять нельзя.
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published',
              'time_create', 'time_update')

    # Только после указания нередактируемых полей
    # их можно добавить в поля (отобразить для чтения).
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')

    # Атрибут добавляет (дублирует) поле УДАЛИТЬ СОХРАНИТЬ сверху формы редактирования.
    save_on_top = True

    # Для отображения фото в таблице Women админ панели.
    # Параметр object - дополнительный параметр
    # (ссылается на текущую запись списка, экземпляр класса Women).
    # Объект self - ссылается на экземпляр класса WomenAdmin.
    def get_html_photo(self, object):

        # Проверяем наличие фото у статьи. Если нет, то вернутся None
        # и джанго поставит прочерк в ячейке.
        if object.photo:

            # Функция mark_safe указывает, что теги должны быть рабочими (они не экранируются).
            return mark_safe(f'<img src="{ object.photo.url }" width="50">')

    # Изменение отображаемого название столбца.
    get_html_photo.short_description = 'Миниатюра'

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

# Заголовок админ панели на вкладке.
admin.site.site_title = 'Админ-панель сайта о женщинах'

# Заголовок админ панели на странице.
admin.site.site_header = 'Админ-панель сайта о женщинах'
