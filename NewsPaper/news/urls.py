from django.urls import path
# Импортируем созданное нами представление
from .views import (BreakingNews, News, Articles, PostCreate, PostDelete, PostUpdate, subscriptions)
# from . import views
from django.urls import path
from .views import IndexView


urlpatterns = [
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    path('index/', IndexView.as_view()),
    path('', News.as_view(), name='news'),
    path('<int:pk>', BreakingNews.as_view(), name='post_detail'),
    path('articles/<int:pk>', Articles.as_view()),
    # path('search/', NewsSearch.as_view(), name='search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    # path('subscriptions/', CategoryListView.as_view(), name='subscriptions')
]

# pk — это первичный ключ товара, который будет выводиться у нас в шаблон
# int — указывает на то, что принимаются только целочисленные значения
