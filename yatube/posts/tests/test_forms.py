from http import HTTPStatus

from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post, User, Comment

COUNT_STEP: int = 1


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Тестовый заголовок 2',
            slug='test-slug-2',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )
        cls.post_create_reverse = reverse('posts:post_create')
        cls.post_edit_reverse = reverse('posts:post_edit', args=[cls.post.pk])
        cls.post_detail_reverse = reverse(
            'posts:post_detail',
            kwargs={'post_id': cls.post.pk}
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create(self):
        """Валидная форма создает запись в Create_post."""
        posts_count = Post.objects.count()
        form_data_1 = {
            'text': 'Тестовый текст',
            'group': self.group.pk,
            'author': self.user,
        }
        response = self.authorized_client.post(
            self.post_create_reverse,
            data=form_data_1,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), posts_count + COUNT_STEP)
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.text, form_data_1['text'])
        self.assertEqual(self.post.group, self.group)

    def test_post_edit(self):
        """Валидная форма изменяет запись в Create_post."""
        form_data_2 = {
            'text': 'Тестовый текст поста 2',
            'group': self.group2.pk,
            'author': self.user
        }
        response = self.authorized_client.post(
            self.post_edit_reverse,
            data=form_data_2,
            follow=True
        )
        self.assertRedirects(
            response,
            self.post_detail_reverse)
        self.assertEqual(self.post.author, form_data_2['author'])
        self.assertNotEqual(self.post.text, form_data_2['text'])
        self.assertNotEqual(self.post.group, form_data_2['group'])

    def test_create_post_page_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        response1 = self.authorized_client.get(self.post_create_reverse)
        response2 = self.authorized_client.get(self.post_edit_reverse)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response1.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
                form_field = response2.context.get('form').fields.get(value)
                self.assertIn('is_edit', response2.context)
                self.assertIsInstance(response2.context['form'], PostForm)
                self.assertIs(response2.context['is_edit'], True)

    def test_post_detail_comment(self):
        '''Валидная форма создает комментарий'''
        comments_count = Comment.objects.count()
        form_data = {
            'text': 'Новый комментарий',
        }
        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        comment = Comment.objects.order_by('-created').first()
        self.assertEqual(Comment.objects.count(), comments_count + COUNT_STEP)
        self.assertEqual(comment.text, form_data['text'])
        self.assertEqual(comment.author, self.user)
