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
        cls.ROUTS = {
            reverse('posts:index'): '/',
            reverse(
                'posts:group_list',
                kwargs={'slug': cls.group.slug}): f'/group/{cls.group.slug}/',
            reverse(
                'posts:profile',
                kwargs={'username': cls.user.username}
            ): f'/profile/{cls.user.username}/',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': cls.post.pk}): f'/posts/{cls.post.pk}/',
            reverse('posts:post_create'): '/create/',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': cls.post.pk}
            ): f'/posts/{cls.post.pk}/edit/',
            reverse(
                'posts:add_comment',
                kwargs={'post_id': cls.post.pk}
            ): f'/posts/{cls.post.pk}/comment/',
            reverse('posts:follow_index'): '/follow/',
            reverse(
                'posts:profile_follow',
                kwargs={'username': cls.user.username}
            ): f'/profile/{cls.user.username}/follow/',
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': cls.user.username}
            ): f'/profile/{cls.user.username}/unfollow/',
        }

    def test_routs(self):
        '''Проверка реверсов'''
        for reverse_name, url_name in self.ROUTS.items():
            self.assertEqual(reverse_name, url_name)
