from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
   text_post = forms.CharField(min_length=20)

   class Meta:
       model = Post
       fields = ['title_post', 'category', 'author', 'text_post']

   def clean(self):
       cleaned_data = super().clean()
       title_post = cleaned_data.get("title_post")
       category = cleaned_data.get("category")
       description = cleaned_data.get("text_post")
       author = cleaned_data.get("author")
       # datetime_post_creation = cleaned_data.get("datetime_post_creation")

       if title_post == category:
           raise ValidationError("A category cannot be identical to title")

       return cleaned_data

   def clean_name(self):
       title_post = self.cleaned_data["title_post"]
       if title_post[0].islower():
           raise ValidationError(
               "Name supposed to begin with a capital letter"
           )
       return title_post
