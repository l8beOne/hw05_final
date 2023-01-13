from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Текст поста',
            'group': 'Группа',
            'image': 'Картинка'
        }
        help_texts = {
            'text': 'Впиши сюда текст поста.',
            'group': 'Определи к какой группе будет относиться пост.',
            'image': 'Загрузите картинку'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
