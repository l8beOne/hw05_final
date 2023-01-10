from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post


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

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        str_dict = {
            self.group.title: str(self.group),
            self.post.text[:Post.POST_LENGHT]: str(self.post),
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
        list_of_verbose_names_dicts = [
            field_verboses_posts,
            field_verboses_groups
        ]
        for dicts in list_of_verbose_names_dicts:
            for field, expected_value in dicts.items():
                with self.subTest(field=field):
                    if dicts == field_verboses_posts:
                        value = Post
                    else:
                        value = Group
                    self.assertEqual(
                        value._meta.get_field(field).verbose_name,
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
        list_of_help_text_dicts = [
            field_help_texts_posts,
            field_help_texts_groups
        ]
        for dicts in list_of_help_text_dicts:
            for field, expected_value in dicts.items():
                with self.subTest(field=field):
                    if dicts == field_help_texts_posts:
                        value = Post
                    else:
                        value = Group
                    self.assertEqual(
                        value._meta.get_field(field).help_text, expected_value)
