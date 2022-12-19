from django.db import models
from django.urls import reverse


# Таблица в БД называется по имени класса.
class Women(models.Model):

    # Поле id автоматически создается из базовоого класса.
    # Общий параметр verbose_name - имя отображения столбца в панели админов.

    # Текстовое поле с максимальной длинной 255 символов
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    # Специальный класс для slug.
    # Параметр unique - означает что поле должно быть уникальным.
    # Параметр db_index=True включает индексацию поля (для ускорения поиска).
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    # Поле с большим количеством текста, ключ blank означает,
    # что поле может быть пустым
    content = models.TextField(blank=True, verbose_name='Текст статьи')

    # Хранит ссылку на изображение, ключ upload_to задает каталог,
    # в который будут загружаться изображения, '%' - текущий
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', verbose_name='Фото')

    # Хранит дату, ключ auto_now_add включает автоматическое определение
    # даты (берется из ОС) в текущий момент и больше никогда не поменяется
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    # Хранит дату, ключ auto_now включает автоматическое определение
    # даты (берется из ОС) в текущий момент при изменении в записи
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    # Хранит bool значение, по умолчанию True
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    # Внешний ключ, будет ссылаться на таблицу Category (первичная модель, Women вторичная),
    # параметр on_delete накладывает ограничения при удалении внешней записи
    # запрещает удаление записи из первичной модели,
    # если она используется во вторичной (выдает исключение)
    # Можно указывать Category как класс без кавычек, но нужно чтобы он был определен перед Women
    # null=True - указывает что поле необязательное, разрешили принимать значение NULL
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    # Магический метод, определяет как будет отображаться экземпляр класса
    # при печати или выводе в приложении.
    def __str__(self):
        return self.title


    # Генерирует абсолютный путь, связывая параметр пути url
    # и атрибут соответствующего экземпляра класса.
    # Помимо того, также много где используется неявно
    # (например, админ панель создает кнопку "посмотреть на сайте").
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # Вложенный класс Meta, используется админ панелью
    # для настройки отображения модели Women.
    # Атрибут verbose_name отображает название модели (таблицы)
    # в таблице приложения Women панели админа.
    # Атрибут verbose_name_plural отображает название модели в таблице
    # панели админа во множественном числе (убирает букву 's').
    # Добавляет порядок сортировки по выбранным полям (в заданом порядке).
    # Знак '-' будет означать инверсию сортировки.
    # На самом сайте данные будут отображаться именно так,
    # как написано в атрибуте ordering.
    class Meta:
        verbose_name = 'статью'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create', 'title']


# Класс для таблицы с категориями (первичная модель)
class Category(models.Model):

    # db_index означает что поле будет проиндексировано, поиск будет происходить несколько быстрее
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'
        ordering = ['id']

