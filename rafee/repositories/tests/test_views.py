import pytest
from mock import patch
from django.core.urlresolvers import reverse

from rest_framework import status

from rafee.test_utils.data import get_data
from rafee.test_utils.assert_helpers import assert_200_and_items_equal
from rafee.test_utils.assert_helpers import assert_status_and_items_equal

from rafee.repositories.tasks import get_dst_path
from rafee.repositories.factories import RepositoryFactory
from rafee.repositories.models import Repository


def test_create(admin_client):
    with patch('rafee.repositories.tasks.GitManager'):
        url = 'http://git.com/blah'
        payload = {'url': url}
        response = admin_client.post(reverse('repository-list'), data=payload)
        assert 'task' in response.data
        queryset = Repository.objects.all()
        assert queryset.filter(url=url).exists()


def test_create_returns_400_if_bad_payload(admin_client):
    payload = {'url': 'not_a_url'}
    response = admin_client.post(reverse('repository-list'), data=payload)
    status_code = status.HTTP_400_BAD_REQUEST
    assert_status_and_items_equal(status_code, ['url'], response)


def test_detail(admin_client):
    repo = RepositoryFactory()
    url = reverse('repository-detail', kwargs={'pk': repo.id})
    response = admin_client.get(url)
    assert_200_and_items_equal(get_data(repo), response)


def generic_test_detail_method_returns_405(client, method):
    __test__ = False
    repo = RepositoryFactory()
    url = reverse('repository-detail', kwargs={'pk': repo.id})
    response = getattr(client, method)(url, data={})
    assert status.HTTP_405_METHOD_NOT_ALLOWED == response.status_code


def test_update_returns_405(admin_client):
    generic_test_detail_method_returns_405(admin_client, method='put')


def test_partial_update_returns_405(admin_client):
    generic_test_detail_method_returns_405(admin_client, method='patch')


def test_delete(admin_client):
    with patch('rafee.repositories.tasks.rmtree') as rmtree_mock:
        repo = RepositoryFactory()
        url = reverse('repository-detail', kwargs={'pk': repo.id})
        response = admin_client.delete(url)
        assert 'task' in response.data
        rmtree_mock.assert_called_with(get_dst_path(repo.url))
        with pytest.raises(Repository.DoesNotExist):
            Repository.objects.get(id=repo.id)
