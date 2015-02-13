import pytest
from mock import patch
from django.core.urlresolvers import reverse
from rest_framework import status

from rafee.test_utils.data import get_data
from rafee.test_utils.assert_helpers import assert_200_and_items_equal
from rafee.test_utils.assert_helpers import assert_201_and_items_equal

from rafee.teams.factories import TeamFactory
from rafee.users.factories import UserFactory
from rafee.users.models import User


@pytest.mark.django_db
@patch('rest_framework_jwt.serializers.authenticate')
def test_auth_token(auth_mock, anon_client):
    user = UserFactory()
    auth_mock.return_value = user
    payload = {
        'username': user.username,
        'password': 'fake',
    }
    response = anon_client.post(reverse('auth-token'), data=payload)
    assert response.data['token']


def test_profile(client, user):
    client.force_authenticate(user=user)
    response = client.get(reverse('user-profile'))
    expected = get_data(user)
    assert_200_and_items_equal(expected, response)


def test_profile_returns_401_if_not_authenticated(anon_client):
    response = anon_client.get(reverse('user-profile'))
    assert status.HTTP_401_UNAUTHORIZED == response.status_code


def test_list(admin_client, admin_user):
    user2 = UserFactory()
    response = admin_client.get(reverse('user-list'))
    expected = [get_data(admin_user), get_data(user2)]
    assert_200_and_items_equal(expected, response)


def test_create(admin_client):
    payload = {
        'username': 'pp',
        'email': 'pp@pp.com',
        'password': '11',
        'full_name': 'pp pp',
        'teams': [TeamFactory().id],
        'is_staff': True,
    }
    response = admin_client.post(reverse('user-list'), data=payload)
    user = User.objects.get(username=response.data['username'])
    assert_201_and_items_equal(get_data(user), response)


def test_create_returns_400_if_duplicate_username(admin_client):
    username = 'pp'
    UserFactory(username=username)
    payload = {
        'username': username,
        'email': 'email@example.com',
        'full_name': 'pp pp',
        'teams': [TeamFactory().id],
        'is_staff': True,
    }
    response = admin_client.post(reverse('user-list'), data=payload)
    assert status.HTTP_400_BAD_REQUEST == response.status_code
    assert 'username' in response.data


def test_detail(admin_client):
    user = UserFactory()
    url = reverse('user-detail', kwargs={'pk': user.pk})
    response = admin_client.get(url)
    assert_200_and_items_equal(get_data(user), response)


def test_update(admin_client):
    user = UserFactory()
    payload = {
        'username': 'pp',
        'email': 'fake@email.com',
        'full_name': user.get_full_name() + ' the third',
        'teams': [TeamFactory().id, TeamFactory().id],
        'is_staff': False,
    }
    url = reverse('user-detail', kwargs={'pk': user.pk})
    response = admin_client.put(url, data=payload)
    updated_user = User.objects.get(pk=response.data['id'])
    assert_200_and_items_equal(get_data(updated_user), response)


def test_partial_update(admin_client):
    user = UserFactory()
    payload = {'full_name': 'New full name'}
    url = reverse('user-detail', kwargs={'pk': user.pk})
    response = admin_client.patch(url, data=payload)
    updated_user = User.objects.get(pk=user.pk)
    assert_200_and_items_equal(get_data(updated_user), response)


def test_delete(admin_client):
    user = UserFactory()
    url = reverse('user-detail', kwargs={'pk': user.pk})
    response = admin_client.delete(url)
    assert status.HTTP_204_NO_CONTENT == response.status_code
    assert response.data is None
    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=user.pk)
