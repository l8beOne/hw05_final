from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Впиши сюда название группы",
        verbose_name="Название"
    )
    slug = models.SlugField(
        help_text="Впиши сюда фрагмент URL-адреса группы",
        unique=True,
        null=True,
        verbose_name="Фрагмент URL-адреса"
    )
    description = models.TextField(
        help_text="Впиши сюда описание группы",
        verbose_name="Описание"
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        help_text="Впиши сюда текст поста",
        verbose_name="Текст поста"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Определи к какой группе будет относиться пост",
        verbose_name="Группа"
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )
    POST_LENGHT = 15

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        help_text="Впиши сюда текст комментария",
        verbose_name="Текст комментария"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации комментария"
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_following')
        ]
