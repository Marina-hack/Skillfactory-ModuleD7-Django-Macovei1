from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.validators import MinValueValidator
# Create your models here.

class Author(models.Model):
    user_author = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)# onetoone(User)
    rating_author = models.SmallIntegerField(default=0)# rating


    def update_rating_author(self):
        postRate = self.post_set.all().aggregate(postRating=Sum('rating_post'))
        pRate = 0
        pRate += postRate.get('postRating')

        commentRate = self.user_author.comment_set.all().aggregate(commentRating=Sum('rating_comment'))
        cRate = 0
        cRate += commentRate.get('commentRating')

        self.rating_author = pRate * 3 + cRate
        self.save()


    def __str__(self):
        return f'{self.user_author}'

# Метод update_rating() модели Author, который обновляет
# рейтинг текущего автора (метод принимает в качестве аргумента только self).
# Он состоит из следующего:
# суммарный рейтинг каждой статьи автора умножается на 3;
# суммарный рейтинг всех комментариев автора;
# суммарный рейтинг всех комментариев к статьям автора.


class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True) # name(unique=True)
# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.). Имеет единственное поле:
# название категории. Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f"{self.name_category}"


class Post(models.Model):
    TYPES = [
        ('AR', 'article'),
        ('NS', 'news'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE,)# onetomany(Author)
    type_post = models.CharField(max_length=2, choices=TYPES, default='AR')# article or news
    datetime_post_creation = models.DateTimeField(auto_now_add=True)# datetime of creation
    category = models.ManyToManyField(Category, through='PostCategory')# manytomany (Category, PostCategory)
    title_post = models.CharField(max_length=128)# title
    text_post = models.TextField()
    rating_post = models.SmallIntegerField(default=0)
    # description = models.TextField()
    # quantity = models.IntegerField(validators=[MinValueValidator(0)],)

    def __str__(self):
        return f'{self.text_post}'

    def like_post(self):
        self.rating_post += 1
        self.save()

    def dislike_post(self):
        self.rating_post -= 1
        self.save()

    def get_absolute_url(self):
        return f'/news/{self.id}'


# rating
# Методы like() и dislike() в моделях Comment и Post,
# которые увеличивают/уменьшают рейтинг на единицу.
    def preview(self):
        return f'{self.text_post[0:123]} + ...'
# Метод preview() модели Post,
# который возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE) # onetomany (Post)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE) # onetomamy (Category)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE) # onetomany(Post)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE) # onetomany(User)
    text_comment = models.TextField()#text comment
    datetime_comment_creation = models.DateTimeField(auto_now_add=True)# datetime of creation
    rating_comment = models.SmallIntegerField(default=0)# rating

    def __str__(self):
        #return f'{self.post_comment.author.user_author.username}, {self.datetime_comment_creation}, {self.text_comment}'
        return f'{self.user_comment}, {self.datetime_comment_creation}, {self.text_comment}'

    def like_comment(self):
        self.rating_comment += 1
        self.save()

    def dislike_comment(self):
        self.rating_comment -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions',)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriptions',)


# Методы like() и dislike() в моделях Comment и Post,
    # которые увеличивают / уменьшают рейтинг на единицу.