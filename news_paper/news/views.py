"""
Данный код представляет собой набор классов представлений для управления новостями в приложении на Django.
Эти представления обеспечивают базовую функциональность CRUD (создание, чтение, обновление, удаление) для
новостного приложения и обеспечивают улучшение пользовательского интерфейса через фильтрацию,
сортировку и пагинацию.

"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Post
from .filters import NewsFilter
from .forms import PostForm


# Отображение списка новостей.
class NewsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Добавляет общее количество новостей в контекст.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_news_count'] = Post.objects.count()
        return context

# Отображение подробной информации о конкретной новости.
class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

# Поиск новостей по заданным фильтрам.
class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
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
class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('news_list')  # Имя маршрута списка новостей


    # Определяет тип поста (новость или статья) и сохраняет его в зависимости от URL.
    def form_valid(self, form):
        post = form.save(commit=False)
        # Определяем тип поста
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
class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


# Удаление поста.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
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
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        return context