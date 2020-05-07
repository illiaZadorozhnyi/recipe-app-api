from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        # create a user
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@ukraine.gov',
            password='password123'
        )
        # log in the user
        self.client.force_login(self.admin_user)
        # create a user that is not logged in
        self.user = get_user_model().objects.create_user(
            email='test@ukraine.gov',
            password='pass123',
            name='Not logged in user full name'
        )

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_edit_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
