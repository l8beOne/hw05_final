from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase

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
        cls.INDEX_URL = '/'
        cls.GROUP_LIST_URL = f'/group/{cls.group.slug}/'
        cls.PROFILE_URL = f'/profile/{cls.user.username}/'
        cls.POST_DETAIL_URL = f'/posts/{cls.post.pk}/'
        cls.CREATE_POST_URL = '/create/'
        cls.POST_EDIT_URL = f'/posts/{cls.post.pk}/edit/'
        cls.FOLLOW = '/follow/'
        cls.UNEXISTING_PAGE = '/unexisting_page/'
        cls.ROUTES_TO_TEMPLATES = {
            cls.INDEX_URL: 'posts/index.html',
            cls.GROUP_LIST_URL: 'posts/group_list.html',
            cls.PROFILE_URL: 'posts/profile.html',
            cls.POST_DETAIL_URL: 'posts/post_detail.html',
            cls.CREATE_POST_URL: 'posts/create_post.html',
            cls.POST_EDIT_URL: 'posts/create_post.html',
            cls.FOLLOW: 'posts/follow.html'
        }
        cls.URL_NAMES_FOR_GUESTS = (
            cls.INDEX_URL,
            cls.GROUP_LIST_URL,
            cls.PROFILE_URL,
            cls.POST_DETAIL_URL,
            cls.UNEXISTING_PAGE,
        )
        cls.LIST_OF_DIFFERENT_CLIENTS = [
            cls.ROUTES_TO_TEMPLATES,
            cls.URL_NAMES_FOR_GUESTS
        ]
        login_then_create = '/auth/login/?next=/create/'
        login_then_edit = f'/auth/login/?next=/posts/{cls.post.pk}/edit/'
        cls.url_redirect_anonymous = {
            login_then_create: '/create/',
            login_then_edit: f'/posts/{cls.post.pk}/edit/',
            f'/posts/{cls.post.pk}/': f'/posts/{cls.post.pk}/edit/'
        }
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(PostURLTests.user)
        cls.nonauthor_client = Client()
        cls.nonauthor_client.force_login(PostURLTests.user2)

    def setUp(self):
        cache.clear()

    def test_url_exists_at_desired_location(self):
        """Страницы доступные гостям и авторизованным пользователям."""
        for dict in self.LIST_OF_DIFFERENT_CLIENTS:
            for address in dict:
                with self.subTest(address=address):
                    if dict == self.URL_NAMES_FOR_GUESTS:
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
        for address, template in self.ROUTES_TO_TEMPLATES.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
