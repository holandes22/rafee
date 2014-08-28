from nose.tools import nottest
from django.core.urlresolvers import reverse

from rest_framework import status

from rafee.test_utils.data import get_data
from rafee.test_utils.base import BaseAPITestCase

from rafee.teams.factories import TeamFactory
from rafee.users.factories import UserFactory

from rafee.users.models import User


class CommonUserTests(BaseAPITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user-detail', kwargs={'email': self.user.email})
        response = self.client.get(url)
        expected = get_data(self.user)
        self.assertResponse200AndItemsEqual(expected, response)

    @nottest
    def generic_test_list_returns_401_if_not_authenticated(self, method):
        url = reverse('user-list')
        response = getattr(self.client, method)(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_get_returns_401_if_not_authenticated(self):
        self.generic_test_list_returns_401_if_not_authenticated('get')

    def test_list_post_returns_401_if_not_authenticated(self):
        self.generic_test_list_returns_401_if_not_authenticated('post')

    @nottest
    def generic_test_detail_returns_401_if_not_authenticated(self, method):
        url = reverse('user-detail', kwargs={'email': self.user.email})
        response = getattr(self.client, method)(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_detail_get_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('get')

    def test_detail_post_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('post')

    def test_detail_put_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('put')

    def test_detail_patch_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('patch')

    def test_detail_delete_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('delete')


class NonAdminUserTests(BaseAPITestCase):

    @nottest
    def generic_test_list_method_returns_403(self, method):
        url = reverse('user-list')
        response = getattr(self.client, method)(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_list_get_returns_403(self):
        self.generic_test_list_method_returns_403('get')

    def test_list_post_returns_403(self):
        self.generic_test_list_method_returns_403('post')

    @nottest
    def generic_test_detail_method_returns_403(self, method):
        url = reverse('user-detail', kwargs={'email': self.user.email})
        response = getattr(self.client, method)(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_update_returns_403(self):
        self.generic_test_detail_method_returns_403('put')

    def test_partial_update_returns_403(self):
        self.generic_test_detail_method_returns_403('patch')

    def test_delete_returns_403(self):
        self.generic_test_detail_method_returns_403('delete')


class AdminUserTests(BaseAPITestCase):

    def setUp(self):
        self.user = UserFactory(is_admin=True)
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        user1 = UserFactory()
        response = self.client.get(reverse('user-list'))
        expected = [get_data(user1), get_data(self.user)]
        self.assertResponse200AndItemsEqual(expected, response)

    def test_create(self):
        payload = {
            'email': 'pp@pp.com',
            'full_name': 'pp pp',
            'team': TeamFactory().id,
            'is_admin': True,
        }
        response = self.client.post(reverse('user-list'), data=payload)
        user = User.objects.get(email=response.data['id'])
        self.assertResponse201AndItemsEqual(get_data(user), response)

    def test_create_returns_400_if_duplicate_email(self):
        email = 'pp@pp.com'
        UserFactory(email=email)
        payload = {
            'email': email,
            'full_name': 'pp pp',
            'team': TeamFactory().id,
            'is_admin': True,
        }
        response = self.client.post(reverse('user-list'), data=payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('email', response.data)

    def test_detail(self):
        user = UserFactory()
        url = reverse('user-detail', kwargs={'email': user.email})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(get_data(user), response)

    def test_update(self):
        pass

    def test_update_returns_500_if_duplicate_email(self):
        pass

    def test_partial_update(self):
        pass

    def test_partial_update_returns_500_if_duplicate_email(self):
        pass

    def test_delete(self):
        pass
