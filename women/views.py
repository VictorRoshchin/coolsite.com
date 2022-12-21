from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

# импорт моделей для получения данных из БД
from .forms import *
from .utils import *
from .models import *


# Класс представления, название придумываем сами. Наследуется от ListView.
class WomenHome(DataMixin, ListView):

    # Класс ListView уже содержит в себе механизм пагинации.
    # Параметр paginate_by указывает количество элементов на одной странице.
    # При использовании класса представления, в шаблон автоматически передаются paginator и page_obj.
    # Параметр paginate_by указан в базовом классе DataMixin для устранения дублирования.

    # Атрибут ссылается на модель Women (список статей).
    # Выбирает все записи записи из таблицы
    # и пытается отобразить в виде списка.
    model = Women

    # Этот атрибут указывает какой шаблон необходимо подгружать.
    template_name = 'women/index.html'

    # Класс представления автоматически генерирует список из БД
    # с названием object_list и передает в шаблон.
    # Этот атрибут меняет название созданного списка.
    context_object_name = 'posts'

    # # Дополнительный передаваемый контекст.
    # # Но таким образом можно передавать только статические (неизменяемые) данные.
    # extra_context = {'title': 'Главная страница'}

    # При помощи функции можно передавать и динамический, и статический контектс.
    def get_context_data(self, *, object_list=None, **kwargs):

        # Чтобы не потерять уже существующий контекст,
        # необходимо первой строчкой обратиться к базовому классу
        # и взять существующий контекст.
        context = super().get_context_data(**kwargs)

        # # Добавляем в контекст menu.
        # context['menu'] = menu

        # context['title'] = 'Главная страница'
        # context['cat_selected'] = 0

        # Вызываем функцию из миксина при помощи self.
        # Формируется словарь c_def с общими параметрами для всех представлений.
        c_def = self.get_user_context(title='Главная страница')

        # Преобразуем items словарей в списки и складываем,
        # затем снова преобразуем в общий словарь
        # и возвращаем его.
        return dict(list(context.items()) + list(c_def.items()))

    # Метод возвращает только те записи,
    # которые должны быть прочитаны из таблицы Women
    # атрибутом model (по заданным требованиям).
    def get_queryset(self):

        # Помимо списка из модели со статьями, дополнительно запрашиваем
        # связанные категории с конкретной записью по ключу cat (связанный параметр).
        # В таком случае при выводе рубрик в шаблоне не будет выполняться дополнительный запрос БД.
        return Women.objects.filter(is_published=True).select_related('cat')


# Функция представления, которая принимает в качестве аргумента http запрос.
def index(request):

    # Берем из таблицы Women все статьи.
    posts = Women.objects.all()

    # Словарь, короторый передается в шаблон.
    context = {
        'posts': posts,
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    # Перенаправляем данные на выбранный шаблон.
    # Автоматически генерируется шаблон и отправляется в качестве ответа.
    return render(request, 'women/index.html', context=context)


# Пример реализации пагинации в функции представлении.
def about(request):

    # Берем список статей из БД.
    contact_list = Women.objects.all()

    # Создаем объект пагинации на основе спика.
    paginator = Paginator(contact_list, 3)

    # Получаем параметр page из запроса на страницу
    page_number = request.GET.get('page')

    # Создаем объект страницы с выбранным номером
    # (получаем из объекта пагинации paginator ту страницу,
    # которая была в запросе при переходе по ссылке,
    # а ссылка находится в шаблоне).
    page_obj = paginator.get_page(page_number)

    # Рендерим данные на шаблон и возвращаем страницу.
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


# Класс для создания формы.
# После отправления формы, данный класс самостоятельно (неявно)
# воспользуется методом get_absolute_url модели Women
# и перейдет на страницу с новой статьей.
class AddPage(LoginRequiredMixin, DataMixin, CreateView):

    # Атрибут указывает адрес, по которому будут перенаправлены неавторизованные пользователи.
    # Чтобы страница могла отобразиться, необходимо выполнить авторизацию, а если пользователь уже
    # авторизован, то перенаправления не произойдет, так работает миксин LoginRequiredMixin.
    # Если представление реализовано при помощи функции,
    # то необходимо использовать декоратор @login_required.
    login_url = reverse_lazy('home')

    # Если этот параметр True, то генерируется ошибка 403 "Доступ запрещен"
    # и перенаправления не происходит.
    raise_exception = True

    # Атрибут указывает на класс, который будет связан
    # с классом представления CreateView.
    form_class = AddPostForm

    template_name = 'women/addpage.html'

    # Если мы не хотим, чтобы было перенаправление на созданную статью.
    # Функция reverse пытается сразу построить маршрут, но django еще его не создал.
    # Функция reverse_lazy строит маршрут только в момент необходимости.
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Вызываем функцию из миксина при помощи self.
        # Формируется словарь c_def с общими параметрами для всех представлений.
        c_def = self.get_user_context(title='Добавление статьи')

        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#
#     # Если запрос был отправлен (была нажата кнопка "отправить", событие submit).
#     if request.method == 'POST':
#
#         # Присваиваем форме значение из полей (словаря request.POST).
#         # Вторым аргументом для сохранения фото передаем коллекцию файлов (request.FILES).
#         form = AddPostForm(request.POST, request.FILES)
#
#         # Если данные из формы прошли проверку.
#         # Если данные не прошли проверку, то будет происходить отображение ошибки.
#         # Данные в форме будут сохраняться и страница будет по обновляться по кругу,
#         # пока проверка не будет пройдена.
#         if form.is_valid():
#
#             # % Для связанной формы.
#             # Сохранения данных из формы в БД.
#             form.save()
#             return redirect('home')
#
#             ## Для несвязанной формы.
#             # try:
#                 # # Пытаемся добавить данные из формы. ** - распаковка в словарь.
#                 # Women.objects.create(**form.cleaned_data)
#
#                 ## Если добавление успешно - происходит переход на главную страницу.
#                 # return redirect('home')
#
#             # except:
#
#                 ## Если произошла ошибка - отображаем эту ошибку на экране перед формой.
#                 ## Добавляем общую ошибку, которая не связана с полями.
#                 # form.add_error(None, 'Ошибка добавления поста')
#
#     # Событие submit еще не произошло (открытие страницы с пустой формой).
#     else:
#
#         # Присваиваем форме (полям формы) пустое значение.
#         form = AddPostForm()
#
#     return render(request, 'women/addpage.html', {'form': form, 'title': 'Добавление статьи'})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    # Метод, который вызывается при успешной проверке формы регистрации.
    # В данном случае автоматическая авторизация.
    def form_valid(self, form):

        # Вывод в консоль на сервере.
        print(form.cleaned_data)

        return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'

    # Переименовывание значения по умолчанию (slug) параметра маршрута.
    slug_url_kwarg = 'post_slug'

    # Для переименовывания параметра маршрута pk (int).
    # pk_url_kwarg = 'post_pk'

    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Вызываем функцию из миксина при помощи self.
        # Формируется словарь c_def с общими параметрами для всех представлений.
        c_def = self.get_user_context(title=context['post'])

        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    # Будет происходить проверка, если в списке нет ни одной записи,
    # то будет генерироваться ошибка 404.
    allow_empty = False

    def get_queryset(self):

        # Через kwargs можно получить все параметры маршрута post (urls),
        # в том числе параметр cat_slag.
        # Два подчеркивания означает, что мы обращаемся к параметру slug таблицы,
        # на которую ссылается параметр cat. Для устранения дополнительго запроса
        # БД сразу же вызываем select_related чтобы добавить связанную со статьей категория.
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)\
            .select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # # Базовый класс уже сформировал параметр posts.
        # # В этой коллекции берем первую запись и возвращаем объект,
        # # затем превращаем его в строку.
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        #
        # context['menu'] = menu
        #
        # # Аналогичным образом как и с названием.
        # context['cat_selected'] = context['posts'][0].cat_id

        # Вызываем функцию из миксина при помощи self.
        # Формируется словарь c_def с общими параметрами для всех представлений.
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)

        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_slug):
#     cat_id = Category.objects.get(slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat_id)
#     cat_title = Category.objects.get(slug=cat_slug)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'title': cat_title,
#         'cat_selected': cat_id.id,
#     }
#
#     return render(request, 'women/index.html', context=context)


class RegisterUser(DataMixin, CreateView):

    # Атрибут ссылается на форму регистрации.
    # UserCreationForm - стандартная (встроенная) форму Джанго.
    # RegisterUserForm - пользовательская форма.
    form_class = RegisterUserForm

    template_name = 'women/register.html'

    # Перенаправление на адрес при успешной регитрации.
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    # Метод, который вызывается при успешной проверке формы регистрации.
    # В данном случае автоматическая авторизация.
    def form_valid(self, form):

        # Пользователь добавляется в БД.
        user = form.save()

        # Производится автоматическая авторизация пользователя при помощи встроенной функции login.
        login(self.request, user)

        # Перенаправление по маршруту.
        return redirect('home')


# Представление формы авторизации. Наследуется от базового класса LoginView.
class LoginUserForm(DataMixin, LoginView):

    # Атрибут ссылается на форму регистрации.
    # В данном случае на стандартную (встроенную) форму Джанго.
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    # Перенаправление при успешной авторизации.
    # Вместо функции можно использовать константу
    # LOGIN_REDIRECT_URL = '<маршрут>' в файле settings.
    def get_success_url(self):
        return reverse_lazy('home')


# Функция для выхода из учетной записи. Операция простая, поэтому реализована через функцию.
def logout_user(request):

    # Используется стандартная функция Джанго.
    logout(request)

    # Перенаправление по маршруту.
    return redirect('login')
