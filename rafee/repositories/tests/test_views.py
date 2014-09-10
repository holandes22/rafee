from django.core.urlresolvers import reverse

from rest_framework import status

from rafee.test_utils.data import get_data
from rafee.test_utils.base import BaseAPITestCase
from rafee.test_utils.base import CommonTestsMixin
from rafee.test_utils.base import NonAdminReadTestsMixin
from rafee.test_utils.base import NonAdminWriteTestsMixin

from rafee.repositories.factories import RepositoryFactory
from rafee.users.factories import UserFactory

from rafee.repositories.models import Repository


class CommonRepositoryTests(CommonTestsMixin, BaseAPITestCase):

    list_url_name = 'repository-list'
    detail_url_name = 'repository-detail'

    def setUp(self):
        self.repo = RepositoryFactory()
        self.detail_url_kwargs = {'id': self.repo.id}


class NonAdminRepositoryTests(NonAdminReadTestsMixin,
                              NonAdminWriteTestsMixin,
                              BaseAPITestCase):

    list_url_name = 'repository-list'
    detail_url_name = 'repository-detail'

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.repo = RepositoryFactory()
        self.detail_url_kwargs = {'id': self.repo.id}


class AdminUserTests(BaseAPITestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        repo = RepositoryFactory()
        response = self.client.get(reverse('repository-list'))
        self.assertResponse200AndItemsEqual([get_data(repo)], response)

    def test_create_returns_a_task(self):
        pass

    def test_create_returns_500_if_bad_url(self):
        pass

    def test_create_adds_scheduled_task_for_pulling(self):
        pass

    def test_create(self):
        payload = {'url': 'http://git.com/blah'}
        response = self.client.post(reverse('repository-list'), data=payload)
        repo = Repository.objects.get(pk=response.data['id'])
        self.assertResponse201AndItemsEqual(get_data(repo), response)

    def test_detail(self):
        repo = RepositoryFactory()
        url = reverse('repository-detail', kwargs={'id': repo.id})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(get_data(repo), response)

    def test_update(self):
        repo = RepositoryFactory(polling_interval=1)
        payload = {'polling_interval': 2}
        url = reverse('repository-detail', kwargs={'id': repo.id})
        response = self.client.put(url, data=payload)
        updated_repo = Repository.objects.get(id=repo.id)
        self.assertResponse200AndItemsEqual(get_data(updated_repo), response)

    def test_update_cannot_modify_url(self):
        repo = RepositoryFactory(url='http://old-url')
        payload = {'polling_interval': 2, 'url': 'http://new-url'}
        url = reverse('repository-detail', kwargs={'id': repo.id})
        response = self.client.put(url, data=payload)
        updated_repo = Repository.objects.get(id=repo.id)
        self.assertEqual(repo.url, response.data['url'])
        self.assertEqual(repo.url, updated_repo.url)

    def test_partial_update(self):
        repo = RepositoryFactory(polling_interval=1)
        payload = {'polling_interval': 2}
        url = reverse('repository-detail', kwargs={'id': repo.id})
        response = self.client.patch(url, data=payload)
        updated_repo = Repository.objects.get(id=repo.id)
        self.assertResponse200AndItemsEqual(get_data(updated_repo), response)

    def test_partial_update_cannot_modify_url(self):
        repo = RepositoryFactory()
        payload = {'url': 'http://new-url'}
        url = reverse('repository-detail', kwargs={'id': repo.id})
        response = self.client.patch(url, data=payload)
        updated_repo = Repository.objects.get(id=repo.id)
        self.assertEqual(repo.url, response.data['url'])
        self.assertEqual(repo.url, updated_repo.url)

    def test_delete(self):
        repo = RepositoryFactory()
        url = reverse('repository-detail', kwargs={'id': repo.id})
        response = self.client.delete(url)
        # Assert folder is also deleted or at least os.rm was called
        # Assert scheduled task was removed
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertIsNone(response.data)
        with self.assertRaises(Repository.DoesNotExist):
            Repository.objects.get(id=repo.id)
