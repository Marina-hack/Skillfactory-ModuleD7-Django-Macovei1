import django_filters
from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')
    added_after = DateTimeFilter(
        field_name='datetime_post_creation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
        model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
        fields = {
           # поиск по названию
            'title_post': ['icontains'],
           # количество товаров должно быть больше или равно
            'category': ['exact']
            # 'datetime_post_creation': ['gt'],
        }

