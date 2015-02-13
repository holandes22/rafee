import pytest
from django.core.urlresolvers import reverse
from rest_framework import status

from rafee.test_utils.data import get_data
from rafee.test_utils.assert_helpers import assert_items_equal
from rafee.test_utils.assert_helpers import assert_200_and_items_equal
from rafee.test_utils.assert_helpers import assert_201_and_items_equal

from rafee.teams.factories import TeamFactory
from rafee.users.factories import UserFactory
from rafee.teams.models import Team


def test_list(admin_client):
    team = TeamFactory()
    response = admin_client.get(reverse('team-list'))
    assert_200_and_items_equal([get_data(team)], response)


def test_list_teams_with_users(admin_client):
    team = TeamFactory()
    user1 = UserFactory(teams=[team])
    user2 = UserFactory(teams=[team])
    response = admin_client.get(reverse('team-list'))
    assert_200_and_items_equal([get_data(team)], response)
    assert_items_equal([user1.id, user2.id], response.data[0]['users'])


def test_create(admin_client):
    payload = {'name': 'The A team'}
    response = admin_client.post(reverse('team-list'), data=payload)
    team = Team.objects.get(pk=response.data['id'])
    assert_201_and_items_equal(get_data(team), response)


def test_detail(admin_client):
    team = TeamFactory()
    UserFactory(teams=[team])
    url = reverse('team-detail', kwargs={'id': team.id})
    response = admin_client.get(url)
    assert_200_and_items_equal(get_data(team), response)


def test_update(admin_client):
    team = TeamFactory(name='old name')
    UserFactory(teams=[team])
    payload = {'name': 'new name'}
    url = reverse('team-detail', kwargs={'id': team.id})
    response = admin_client.put(url, data=payload)
    updated_team = Team.objects.get(id=team.id)
    assert_200_and_items_equal(get_data(updated_team), response)


def test_update_team_users(admin_client):
    team = TeamFactory(name='old name')
    UserFactory(teams=[team])
    new_user = UserFactory()
    payload = {'name': 'new name', 'users': [new_user.id]}
    url = reverse('team-detail', kwargs={'id': team.id})
    admin_client.put(url, data=payload)
    updated_team = Team.objects.get(id=team.id)
    assert new_user.username == updated_team.users.all()[0].username


def test_partial_update(admin_client):
    team = TeamFactory(name='old name')
    payload = {'name': 'new name'}
    url = reverse('team-detail', kwargs={'id': team.id})
    response = admin_client.patch(url, data=payload)
    updated_team = Team.objects.get(id=team.id)
    assert_200_and_items_equal(get_data(updated_team), response)


def test_delete(admin_client):
    team = TeamFactory()
    url = reverse('team-detail', kwargs={'id': team.id})
    response = admin_client.delete(url)
    assert status.HTTP_204_NO_CONTENT == response.status_code
    assert response.data is None
    with pytest.raises(Team.DoesNotExist):
        Team.objects.get(id=team.id)
