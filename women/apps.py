from django.apps import AppConfig


# Этот класс используется для конфигурации всего приложения Women.
# Атрибуты данного класса будут автоматически сработают в админ панели только в том случае,
# если приложение Women зарегистрированое в файле settings как 'women.apps.WomenConfig'
# (с использованием WomenConfig).
class WomenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'

    # Атрибут verbose_name отображает название приложения Women
    # в панели админа (заголовок таблицы).
    verbose_name = 'Женщины мира'
