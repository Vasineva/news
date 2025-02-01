from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, PostCreate, PostUpdate, PostDelete, IndexView


urlpatterns = [
    path('', IndexView.as_view()),
    path('posts/', NewsList.as_view(), name='news_list'),
    path('posts/<int:id>/', NewsDetail.as_view(), name='news_detail'),
    path('posts/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('posts/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

]
