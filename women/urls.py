from django.urls import path, re_path
from .views import *

# Импортируем декоратор класса для кэширования.
from django.views.decorators.cache import cache_page

urlpatterns = [

    # name используется для машрутизации (это имя внутри проекта адреса)

    # Можно использовать кэш на уровне шаблонов:
    # {% load cache %} - в шапке. И в заключить нужный фрагмент документа в:
    # {% cache <secs> <name> %} ... {% endcache %}
    # Использование кэширования представления всей страницы.
    # path('', cache_page(60)(WomenHome.as_view()), name='home'),

    # Чтобы класс связать с маршрутом нужно вызвать спеециальную функцию as_view().
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUserForm.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]
