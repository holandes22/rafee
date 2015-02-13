import pytest
from rest_framework import status
from django.core.urlresolvers import reverse

from rafee.users.factories import UserFactory
from rafee.teams.factories import TeamFactory
from rafee.slideshows.factories import SlideshowFactory
from rafee.repositories.factories import RepositoryFactory


# pylint: disable=invalid-name


test_params = [
    (UserFactory, 'pk'),
    (TeamFactory, 'id'),
    (SlideshowFactory, 'id'),
    (RepositoryFactory, 'pk'),
]


@pytest.fixture(params=test_params)
def detail_url(request, db):
    factory_cls, lookup_field = request.param
    obj = factory_cls()
    detail_url_name = '{}-detail'.format(obj.__class__.__name__.lower())
    kwargs = {lookup_field: getattr(obj, lookup_field)}
    return reverse(detail_url_name, kwargs=kwargs)


@pytest.fixture(params=['user', 'team', 'slideshow', 'repository', 'template'])
def list_url(request):
    list_url_name = '{}-list'.format(request.param)
    return reverse(list_url_name)


pytestmark = pytest.mark.django_db

# Test list errors


def test_list_get_returns_401_if_not_authenticated(anon_client, list_url):
    response = anon_client.get(list_url)
    assert status.HTTP_401_UNAUTHORIZED == response.status_code


def test_list_post_returns_401_if_not_authenticated(anon_client, list_url):
    response = anon_client.post(list_url)
    assert status.HTTP_401_UNAUTHORIZED == response.status_code


def test_list_put_returns_405(admin_client, list_url):
    response = admin_client.put(list_url)
    assert status.HTTP_405_METHOD_NOT_ALLOWED == response.status_code


def test_list_patch_returns_405(admin_client, list_url):
    response = admin_client.patch(list_url)
    assert status.HTTP_405_METHOD_NOT_ALLOWED == response.status_code


def test_list_delete_returns_405(admin_client, list_url):
    response = admin_client.delete(list_url)
    assert status.HTTP_405_METHOD_NOT_ALLOWED == response.status_code


def test_list_get_returns_403_if_non_admin(client, list_url):
    response = client.get(list_url)
    assert status.HTTP_403_FORBIDDEN == response.status_code


def test_list_post_returns_403_if_non_admin(client, list_url):
    response = client.post(list_url)
    assert status.HTTP_403_FORBIDDEN == response.status_code


# Test detail errors


def test_detail_get_returns_401_if_anonymous(anon_client, detail_url):
    response = anon_client.get(detail_url)
    assert status.HTTP_401_UNAUTHORIZED == response.status_code


def test_detail_post_returns_401_if_anonymous(anon_client, detail_url):
    response = anon_client.post(detail_url)
    assert status.HTTP_401_UNAUTHORIZED == response.status_code


def test_detail_put_returns_401_if_anonymous(anon_client, detail_url):
    response = anon_client.put(detail_url)
    assert status.HTTP_401_UNAUTHORIZED == response.status_code


def test_detail_patch_returns_401_if_anonymous(anon_client, detail_url):
    response = anon_client.patch(detail_url)
    assert status.HTTP_401_UNAUTHORIZED == response.status_code


def test_detail_delete_returns_401_if_anonymous(anon_client, detail_url):
    response = anon_client.delete(detail_url)
    assert status.HTTP_401_UNAUTHORIZED == response.status_code


def test_detail_post_returns_405(admin_client, detail_url):
    response = admin_client.post(detail_url)
    assert status.HTTP_405_METHOD_NOT_ALLOWED == response.status_code


def test_detail_get_returns_403(client, detail_url):
    response = client.get(detail_url)
    assert status.HTTP_403_FORBIDDEN == response.status_code


def test_detail_put_returns_403(client, detail_url):
    response = client.put(detail_url)
    assert status.HTTP_403_FORBIDDEN == response.status_code


def test_detail_patch_returns_403(client, detail_url):
    response = client.patch(detail_url)
    assert status.HTTP_403_FORBIDDEN == response.status_code


def test_detail_delete_returns_403(client, detail_url):
    response = client.delete(detail_url)
    assert status.HTTP_403_FORBIDDEN == response.status_code
