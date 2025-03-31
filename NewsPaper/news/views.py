"""
Данный код представляет собой набор классов представлений для управления новостями в приложении на Django.
Эти представления обеспечивают базовую функциональность CRUD (создание, чтение, обновление, удаление) для
новостного приложения и обеспечивают улучшение пользовательского интерфейса через фильтрацию,
сортировку и пагинацию.

"""
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, PermissionDenied


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Post, Author, Category
from .filters import NewsFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.cache import cache # импортируем наш кэш
from django.utils.translation import gettext as _ # импортируем функцию для перевода
from django.http import HttpResponse
from django.views import View

# Create your views here.

class Index(View):
    def get(self, request):
        string = _('Hello world')
        return HttpResponse(string)

# Отображение списка новостей.
class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'post/news.html'
    context_object_name = 'posts'
    paginate_by = 10


    # Добавляет общее количество новостей в контекст.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_news_count'] = Post.objects.count()
        return context


class CategoryList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'post/news_category.html'
    context_object_name = 'news'
    paginate_by = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.category = Category.objects.get(pk=self.kwargs.get('pk'))
        queryset = queryset.filter(categories=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# Отображение подробной информации о конкретной новости.
class NewsDetail(DetailView):
    model = Post
    template_name = 'post/news_detail.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj

# Поиск новостей по заданным фильтрам.
class NewsSearch(ListView):
    model = Post
    template_name = 'post/news_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    #  Переопределяет метод для применения фильтров.
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    # Добавляет фильтр в контекст для отображения.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

# Создание нового поста.
class PostCreate(PermissionRequiredMixin,LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post/post_create.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        author, created = Author.objects.get_or_create(user=self.request.user)
        post.author = author

        # Определяем тип поста (новость или статья)
        if 'news' in self.request.path:
            post.post_type = 'NW'
        else:
            post.post_type = 'AR'

        post.save()
        return super().form_valid(form)

    # Передает информацию о типе поста в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'news' in self.request.path:
            context['post_type'] = "Новость"
        else:
            context['post_type'] = "Статья"
        return context

# Обновление существующего поста.
class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post/post_create.html'
    permission_required = ('news.change_post')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author.user != self.request.user:
            raise PermissionDenied
        return obj


# Удаление поста.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('news_list') # URL для перенаправления после удаления поста.

    # Передает тип поста в контекст.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = self.object.get_post_type_display()
        return context


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    is_subscriber = Category.objects.get(pk=pk)
    if not user.subscribers.filter(pk=pk).exists():
        is_subscriber.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))


