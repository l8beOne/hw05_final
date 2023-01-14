from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Comment, Follow, Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
            pub_date='Дата публикации',
        )
        cls.comment = Comment.objects.create(
            text='Тестовый коммент',
            author=cls.user,
            post=cls.post
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        str_dict = {
            self.group.title: str(self.group),
            self.post.text[:Post.POST_LENGHT]: str(self.post),
            self.comment.text[:Comment.COMMENT_LENGHT]: str(self.comment)
        }
        for field, expected_value in str_dict.items():
            with self.subTest(field=field):
                self.assertEqual(
                    field, expected_value)

    def test_posts_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses_posts = {
            'text': 'Текст поста',
            'author': 'Автор',
            'group': 'Группа',
            'pub_date': 'Дата публикации',
        }
        field_verboses_groups = {
            'title': 'Название',
            'slug': 'Фрагмент URL-адреса',
            'description': 'Описание',
        }
        field_verboses_comments = {
            'post': 'Пост, под которым оставлен комментарий',
            'author': 'Автор комментария',
            'text': 'Текст комментария',
            'created': 'Дата публикации комментария',
        }
        field_verboses_follows = {
            'user': 'Подписчик',
            'author': 'Автор',
        }
        dict_of_verbose_names_dicts = {
            Post: field_verboses_posts,
            Group: field_verboses_groups,
            Comment: field_verboses_comments,
            Follow: field_verboses_follows
        }
        for classes, dicts in dict_of_verbose_names_dicts.items():
            for field, expected_value in dicts.items():
                with self.subTest(field=field):
                    self.assertEqual(
                        classes._meta.get_field(field).verbose_name,
                        expected_value
                    )

    def test_help_text_posts(self):
        """help_text в полях совпадает с ожидаемым."""
        field_help_texts_posts = {
            'text': 'Впиши сюда текст поста',
            'group': 'Определи к какой группе будет относиться пост',
        }
        field_help_texts_groups = {
            'title': 'Впиши сюда название группы',
            'slug': 'Впиши сюда фрагмент URL-адреса группы',
            'description': 'Впиши сюда описание группы'
        }
        field_help_texts_comments = {
            'text': 'Впиши сюда текст комментария'
        }
        dict_of_help_text_dicts = {
            Post: field_help_texts_posts,
            Group: field_help_texts_groups,
            Comment: field_help_texts_comments,
        }
        for classes, dicts in dict_of_help_text_dicts.items():
            for field, expected_value in dicts.items():
                with self.subTest(field=field):
                    self.assertEqual(
                        classes._meta.get_field(field).help_text,
                        expected_value
                    )
