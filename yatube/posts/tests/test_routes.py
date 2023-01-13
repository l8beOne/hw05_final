from django.test import TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostRoutesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
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
        cls.ROUTS = {
            cls.REVERSE_INDEX: '/',
            cls.REVERSE_GROUP_LIST: f'/group/{cls.group.slug}/',
            cls.REVERSE_PROFILE: f'/profile/{cls.user.username}/',
            cls.REVERSE_POST_DETAIL: f'/posts/{cls.post.pk}/',
            cls.REVERSE_POST_CREATE: '/create/',
            cls.REVERSE_POST_EDIT: f'/posts/{cls.post.pk}/edit/',
            cls.REVERSE_ADD_COMMENT: f'/posts/{cls.post.pk}/comment/',
            cls.REVERSE_FOLLOW_INDEX: '/follow/',
            cls.PROFILE_FOLLOW: f'/profile/{cls.user.username}/follow/',
            cls.PROFILE_UNFOLLOW: f'/profile/{cls.user.username}/unfollow/',
        }

    def test_routs(self):
        '''Проверка реверсов'''
        for reverse_name, url_name in self.ROUTS.items():
            self.assertEqual(reverse_name, url_name)
