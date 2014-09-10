from django.core.urlresolvers import reverse

from rest_framework import status

from rafee.test_utils.data import get_data
from rafee.test_utils.base import BaseAPITestCase
from rafee.test_utils.base import CommonTestsMixin
from rafee.test_utils.base import NonAdminListReadTestsMixin
from rafee.test_utils.base import NonAdminWriteTestsMixin

from rafee.teams.factories import TeamFactory
from rafee.users.factories import UserFactory

from rafee.users.models import User


class CommonUserTests(CommonTestsMixin, BaseAPITestCase):

    list_url_name = 'user-list'
    detail_url_name = 'user-detail'

    def setUp(self):
        self.user = UserFactory()
        self.detail_url_kwargs = {'email': self.user.email}

    def test_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(self.detail_url_name, kwargs=self.detail_url_kwargs)
        response = self.client.get(url)
        expected = get_data(self.user)
        self.assertResponse200AndItemsEqual(expected, response)


class NonAdminUserTests(NonAdminListReadTestsMixin,
                        NonAdminWriteTestsMixin,
                        BaseAPITestCase):

    list_url_name = 'user-list'
    detail_url_name = 'user-detail'

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.detail_url_kwargs = {'email': self.user.email}


class AdminUserTests(BaseAPITestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        user1 = UserFactory()
        response = self.client.get(reverse('user-list'))
        expected = [get_data(user1), get_data(self.user)]
        self.assertResponse200AndItemsEqual(expected, response)

    def test_create(self):
        payload = {
            'username': 'pp',
            'email': 'pp@pp.com',
            'password': '11',
            'full_name': 'pp pp',
            'teams': [TeamFactory().id],
            'is_staff': True,
        }
        response = self.client.post(reverse('user-list'), data=payload)
        user = User.objects.get(username=response.data['username'])
        self.assertResponse201AndItemsEqual(get_data(user), response)

    def test_create_returns_400_if_duplicate_username(self):
        username = 'pp'
        UserFactory(username=username)
        payload = {
            'username': username,
            'email': 'email@example.com',
            'full_name': 'pp pp',
            'teams': [TeamFactory().id],
            'is_staff': True,
        }
        response = self.client.post(reverse('user-list'), data=payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('username', response.data)

    def test_detail(self):
        user = UserFactory()
        url = reverse('user-detail', kwargs={'email': user.email})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(get_data(user), response)

    def test_update(self):
        user = UserFactory()
        payload = {
            'username': 'pp',
            'email': 'fake@email.com',
            'full_name': user.get_full_name() + ' the third',
            'teams': [TeamFactory().id, TeamFactory().id],
            'is_staff': False,
        }
        url = reverse('user-detail', kwargs={'email': user.email})
        response = self.client.put(url, data=payload)
        # email should not have been updated
        updated_user = User.objects.get(email=user.email)
        self.assertResponse200AndItemsEqual(get_data(updated_user), response)

    def test_partial_update(self):
        user = UserFactory()
        payload = {'full_name': 'New full name'}
        url = reverse('user-detail', kwargs={'email': user.email})
        response = self.client.patch(url, data=payload)
        updated_user = User.objects.get(email=user.email)
        self.assertResponse200AndItemsEqual(get_data(updated_user), response)

    def test_delete(self):
        user = UserFactory()
        url = reverse('user-detail', kwargs={'email': user.email})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertIsNone(response.data)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=user.email)
