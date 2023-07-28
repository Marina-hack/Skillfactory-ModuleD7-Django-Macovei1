from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect
from .models import Post, Subscription, Category
from datetime import datetime, timedelta
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.views import View
from .tasks import printer, hello


class IndexView(View):
    def get(self, request):
        # printer.delay(10)
        # hello.delay()
        # return HttpResponse('Hello!')
        printer.apply_async([10],
                            eta=datetime.now() + timedelta(seconds=5))
        hello.delay()
        return HttpResponse('Hello!')
# выполнить задачу hello (метод delay()) и вернуть только 'Hello!' в браузер.
# Здесь мы использовали класс-представление. В методе get() мы написали действия,
# которые хотим выполнить при вызове этого представления


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category,).delete()

    message = "Subscription has been added successfully"
    categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(Subscription.objects.filter(user=request.user, category=OuterRef('pk'),))).order_by('name_category')
    return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions, 'message': message})


class News(ListView):
    model = Post
    ordering = '-datetime_post_creation' #сортировка по дате создания
    # queryset = Post.objects.post_by('name')
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # context['time_now'] = datetime.utcnow()
        return context

 
class BreakingNews(DetailView):
    model = Post
    template_name = 'breaking_news.html'
    context_object_name = 'breaking_news'


class Articles(DetailView):
    model = Post
    template_name = 'articles.html'
    context_object_name = 'articles'


class PostCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    permission_required = ('news.add_post',)
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news')


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')


# class CategoryListView(ListView):
#     model = Post
#     template_name = 'subscriptions.html' #название шаблона
#     context_object_name = 'subscriptions'
#
#     def get_queryset(self):
#         self.category = get_object_or_404(Category, id=self.kwargs['pk'])
#         queryset = Post.objects.filter(category=self.category).order_by('-date')
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
#         context['category'] = self.category
#         return context
