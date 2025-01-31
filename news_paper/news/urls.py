from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:id>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
]
