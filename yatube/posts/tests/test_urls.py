from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus as status_code

from ..models import Post, Group

User = get_user_model()


class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности статичных адресов."""
        static_pages_urls = ('/about/author/', '/about/tech/')
        for value in static_pages_urls:
            response = self.guest_client.get(value)
            with self.subTest(value=value):
                self.assertEqual(response.status_code, status_code.OK)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблонов для статичных адресов."""
        static_pages_templates = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for value, expected in static_pages_templates.items():
            response = self.guest_client.get(value)
            with self.subTest(value=value):
                self.assertTemplateUsed(
                    response, expected)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_author = User.objects.create(
            username='test',
            email='test@example.com',
        )
        test_group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        test_post = Post.objects.create(
            id=1,
            text='Тестовый текст',
            author=test_author,
            group=test_group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_url_exists_at_desired_location(self):
        """Тест доступа к общедоступным страницам."""
        public_pages = (
            '/',
            '/group/test-slug/',
            '/profile/HasNoName/',
            '/posts/1/',
        )
        for value in public_pages:
            response = self.guest_client.get(value)
            with self.subTest(value=value):
                self.assertEqual(response.status_code, status_code.OK)
