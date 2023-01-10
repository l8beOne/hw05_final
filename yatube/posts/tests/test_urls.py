from http import HTTPStatus

from django.test import Client, TestCase
from django.core.cache import cache

from posts.models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.user2 = User.objects.create(username='nonauthor')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )
        cls.routes_to_templates = {
            '/': 'posts/index.html',
            f'/group/{cls.group.slug}/': 'posts/group_list.html',
            f'/profile/{cls.user.username}/': 'posts/profile.html',
            f'/posts/{cls.post.pk}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{cls.post.pk}/edit/': 'posts/create_post.html'
        }
        cls.url_names_for_guests = (
            '/',
            f'/group/{cls.group.slug}/',
            f'/profile/{cls.user.username}/',
            f'/posts/{cls.post.pk}/',
            '/unexisting_page/',
        )
        cls.list_of_difrnt_clients = [
            cls.routes_to_templates,
            cls.url_names_for_guests
        ]
        login_then_create = '/auth/login/?next=/create/'
        login_then_edit = f'/auth/login/?next=/posts/{cls.post.pk}/edit/'
        cls.url_redirect_anonymous = {
            login_then_create: '/create/',
            login_then_edit: f'/posts/{cls.post.pk}/edit/',
            f'/posts/{cls.post.pk}/': f'/posts/{cls.post.pk}/edit/'
        }

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='User')
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)
        self.nonauthor_client = Client()
        self.nonauthor_client.force_login(PostURLTests.user2)
        cache.clear()

    def test_url_exists_at_desired_location(self):
        """Страницы доступные гостям и авторизованным пользователям."""
        for dict in self.list_of_difrnt_clients:
            for address in dict:
                with self.subTest(address=address):
                    if dict == self.url_names_for_guests:
                        client = self.guest_client
                        if address == '/unexisting_page/':
                            httpstatus = HTTPStatus.NOT_FOUND
                    else:
                        client = self.authorized_client
                        httpstatus = HTTPStatus.OK
                    response = client.get(address)
                    self.assertEqual(response.status_code, httpstatus)

    def test_create_list_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /create/, /post/edit/ перенаправит анонимного
        пользователя на страницу логина.
        """
        for redirect_url, address in self.url_redirect_anonymous.items():
            with self.subTest(address=address):
                if redirect_url == f'/posts/{self.post.pk}/':
                    client = self.nonauthor_client
                else:
                    client = self.guest_client
                response = client.get(address)
                self.assertRedirects(response, redirect_url)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for address, template in self.routes_to_templates.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)