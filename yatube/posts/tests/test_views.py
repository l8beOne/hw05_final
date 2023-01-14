from django.conf import settings
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import CommentForm
from posts.models import Comment, Follow, Group, Post, User


class PaginatorViewsTest(TestCase):
    TEST_OF_POST = 13

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group')
        posts = [Post(
            text=f'Тестовый текст {i}',
            group=cls.group,
            author=cls.user) for i in range(cls.TEST_OF_POST)]
        cls.posts = Post.objects.bulk_create(posts)
        cls.REVERSE_PAGES = (
            reverse('posts:index'),
            reverse(
                'posts:profile',
                kwargs={'username': f'{cls.user.username}'}
            ),
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{cls.group.slug}'}
            )
        )
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def setUp(self):
        cache.clear()

    def test_correct_page_context_guest_client(self):
        '''Проверка количества постов на первой и второй страницах. '''
        for page in self.REVERSE_PAGES:
            ARGUMENTS_FOR_PAGES = (
                page,
                page + '?page=2'
            )
            for args in ARGUMENTS_FOR_PAGES:
                response = self.guest_client.get(args)
                count_posts = len(response.context['page_obj'])
                if args == page:
                    self.assertEqual(
                        count_posts,
                        settings.POSTS_ON_PAGE,
                    )
                else:
                    self.assertEqual(
                        count_posts,
                        self.TEST_OF_POST - settings.POSTS_ON_PAGE
                    )


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.follower = User.objects.create(username='IwantFollow')
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
        cls.comment = Comment.objects.create(
            text='Тестовый коммент',
            author=cls.user,
            post=cls.post
        )
        cls.REVERSE_INDEX = reverse('posts:index')
        cls.REVERSE_GROUP_LIST = reverse(
            'posts:group_list',
            kwargs={'slug': cls.group.slug}
        )
        cls.REVERSE_PROFILE = reverse(
            'posts:profile',
            kwargs={'username': cls.user.username}
        )
        cls.REVERSE_POST_DETAIL = reverse(
            'posts:post_detail',
            kwargs={'post_id': cls.post.pk}
        )
        cls.REVERSE_POST_CREATE = reverse('posts:post_create')
        cls.REVERSE_POST_EDIT = reverse(
            'posts:post_edit',
            kwargs={'post_id': cls.post.pk}
        )
        cls.REVERSE_ADD_COMMENT = reverse(
            'posts:add_comment',
            kwargs={'post_id': cls.post.pk}
        )
        cls.REVERSE_FOLLOW_INDEX = reverse('posts:follow_index')
        cls.PROFILE_FOLLOW = reverse(
            'posts:profile_follow',
            kwargs={'username': cls.user.username}
        )
        cls.PROFILE_UNFOLLOW = reverse(
            'posts:profile_unfollow',
            kwargs={'username': cls.user.username}
        )
        cls.VALUE_OF_EVERY_PAGE = {
            cls.REVERSE_INDEX: 'page_obj',
            cls.REVERSE_GROUP_LIST: 'page_obj',
            cls.REVERSE_PROFILE: 'page_obj',
            cls.REVERSE_POST_DETAIL: 'post',
        }
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(PostURLTests.user)
        cls.client_become_follower = Client()
        cls.client_become_follower.force_login(cls.follower)

    def setUp(self):
        cache.clear()

    def test_index_page_show_correct_context(self):
        """Шаблон index, group_list, profile, post_detail
        сформированы с правильным контекстом."""
        for reverse_name, context_value in self.VALUE_OF_EVERY_PAGE.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                if context_value != 'post':
                    first_object = response.context[context_value][0]
                else:
                    first_object = response.context[context_value]
                    self.assertIsInstance(
                        response.context['form'],
                        CommentForm
                    )
                    self.assertEqual(
                        response.context['comments'][0],
                        self.comment
                    )
                self.assertEqual(first_object.text, self.post.text)
                self.assertEqual(first_object.author, self.post.author)
                self.assertEqual(first_object.group, self.post.group)
                self.assertEqual(first_object.pk, self.post.pk)
                self.assertEqual(first_object.image, self.post.image)

    def test_post_added_correctly(self):
        """Пост при создании добавлен корректно"""
        response_index = self.authorized_client.get(self.REVERSE_INDEX)
        response_group = self.authorized_client.get(self.REVERSE_GROUP_LIST)
        response_profile = self.authorized_client.get(self.REVERSE_PROFILE)
        index = response_index.context['page_obj']
        group = response_group.context['page_obj']
        profile = response_profile.context['page_obj']
        self.assertIn(self.post, index)
        self.assertIn(self.post, group)
        self.assertIn(self.post, profile)

    def test_cache_run(self):
        post = Post.objects.create(
            text='Проверка кэша',
            author=self.user,
            group=self.group
        )
        response_add = self.authorized_client.get(self.REVERSE_INDEX).content
        post.delete()
        response_delete = self.authorized_client.get(
            self.REVERSE_INDEX).content
        self.assertEqual(response_add, response_delete)
        cache.clear()
        response_cache_cleared = self.authorized_client.get(
            self.REVERSE_INDEX).content
        self.assertNotEqual(response_add, response_cache_cleared)

    def test_user_become_follower(self):
        '''Авторизованный пользователь может подписываться на пользователей'''
        follows_count = Follow.objects.count()
        self.client_become_follower.get(self.PROFILE_FOLLOW)
        self.assertEqual(Follow.objects.count(), follows_count + 1)

    def test_user_unfollow(self):
        '''Авторизованный пользователь может отписываться от пользователей'''
        follows_count = Follow.objects.count()
        new_follower = Follow.objects.create(
            user=self.follower,
            user_id=self.follower.pk,
            author=self.user)
        new_follower.delete()
        follower_id = new_follower.pk
        self.client_become_follower.get(self.PROFILE_UNFOLLOW)
        self.assertEqual(Follow.objects.count(), follows_count)
        self.assertFalse(Follow.objects.filter(
            user=self.follower,
            user_id=follower_id,
            author=self.user).exists())

    def test_follow_on_user(self):
        """Новая запись пользователя появляется в ленте у подписчиков
         и не появляется у неподписанных"""
        Follow.objects.create(
            user=self.follower,
            author=self.user)
        response_follower = self.client_become_follower.get(
            self.REVERSE_FOLLOW_INDEX)
        response_not_follower = self.authorized_client.get(
            self.REVERSE_FOLLOW_INDEX)
        self.assertIn(self.post, response_follower.context['page_obj'])
        self.assertNotIn(
            self.post,
            response_not_follower.context['page_obj']
        )
