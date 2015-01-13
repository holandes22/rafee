from mock import patch
from django.core.urlresolvers import reverse

from rest_framework import status

from rafee.test_utils.data import get_data
from rafee.test_utils.base import BaseAPITestCase
from rafee.test_utils.base import CommonTestsMixin
from rafee.test_utils.base import NonAdminReadTestsMixin
from rafee.test_utils.base import NonAdminWriteTestsMixin

from rafee.repositories.tasks import get_dst_path
from rafee.repositories.factories import RepositoryFactory
from rafee.users.factories import UserFactory
from rafee.repositories.models import Repository


class CommonRepositoryTests(CommonTestsMixin, BaseAPITestCase):

    list_url_name = 'repository-list'
    detail_url_name = 'repository-detail'

    def extra_setup(self):
        self.repo = RepositoryFactory()
        self.detail_url_kwargs = {'pk': self.repo.id}


class NonAdminRepositoryTests(NonAdminReadTestsMixin,
                              NonAdminWriteTestsMixin,
                              BaseAPITestCase):

    list_url_name = 'repository-list'
    detail_url_name = 'repository-detail'

    def extra_setup(self):
        self.repo = RepositoryFactory()
        self.detail_url_kwargs = {'pk': self.repo.id}


class AdminUserTests(BaseAPITestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        repo = RepositoryFactory()
        response = self.client.get(reverse('repository-list'))
        self.assertResponse200AndItemsEqual([get_data(repo)], response)

    @patch('rafee.repositories.tasks.GitManager')
    def test_create(self, gm_mock):
        url = 'http://git.com/blah'
        payload = {'url': url}
        response = self.client.post(reverse('repository-list'), data=payload)
        self.assertIn('task', response.data)
        queryset = Repository.objects.all()
        self.assertTrue(queryset.filter(url=url).exists())

    def test_create_returns_400_if_bad_payload(self):
        payload = {'url': 'not_a_url'}
        response = self.client.post(reverse('repository-list'), data=payload)
        status_code = status.HTTP_400_BAD_REQUEST
        self.assertResponseStatusAndItemsEqual(status_code, ['url'], response)

    def test_detail(self):
        repo = RepositoryFactory()
        url = reverse('repository-detail', kwargs={'pk': repo.id})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(get_data(repo), response)

    def generic_test_detail_method_returns_405(self, method):
        __test__ = False
        repo = RepositoryFactory()
        url = reverse('repository-detail', kwargs={'pk': repo.id})
        response = getattr(self.client, method)(url, data={})
        self.assertEqual(
            status.HTTP_405_METHOD_NOT_ALLOWED,
            response.status_code,
        )

    def test_update_returns_405(self):
        self.generic_test_detail_method_returns_405(method='put')

    def test_partial_update_returns_405(self):
        self.generic_test_detail_method_returns_405(method='patch')

    @patch('rafee.repositories.tasks.rmtree')
    def test_delete(self, rmtree_mock):
        repo = RepositoryFactory()
        url = reverse('repository-detail', kwargs={'pk': repo.id})
        response = self.client.delete(url)
        self.assertIn('task', response.data)
        rmtree_mock.assert_called_with(get_dst_path(repo.url))
        with self.assertRaises(Repository.DoesNotExist):
            Repository.objects.get(id=repo.id)
