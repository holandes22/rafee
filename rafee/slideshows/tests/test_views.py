import pytest
from mock import patch
from django.core.urlresolvers import reverse

from rest_framework import status

from rafee.messages import TEMPLATES_NOT_FOUND
from rafee.test_utils.data import get_data

from rafee.teams.factories import TeamFactory
from rafee.users.factories import UserFactory
from rafee.slideshows.factories import SlideshowFactory

from rafee.slideshows.models import Slideshow
from rafee.test_utils.assert_helpers import assert_items_equal
from rafee.test_utils.assert_helpers import assert_200_and_items_equal
from rafee.test_utils.assert_helpers import assert_201_and_items_equal
from rafee.test_utils.assert_helpers import assert_status_and_items_equal

# pylint: disable=redefined-outer-name,invalid-name


def assert_expected_duplicate_name(response):
    expected = {
        'non_field_errors': [
            'Slideshow with this Name and Team already exists.'
        ],
    }
    assert_status_and_items_equal(
        status.HTTP_400_BAD_REQUEST, expected, response
    )


@pytest.fixture
def slideshow(user):
    team = TeamFactory()
    user.teams.add(team)
    return SlideshowFactory(team=team)


def test_list(client, slideshow):
    assert_200_and_items_equal(
        [get_data(slideshow)],
        client.get(reverse('slideshow-list'))
    )


def test_list_returns_slideshows_from_the_user_team(client, slideshow):
    SlideshowFactory()
    response = client.get(reverse('slideshow-list'))
    assert_200_and_items_equal([get_data(slideshow)], response)


def test_detail(client, slideshow):
    url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
    response = client.get(url)
    assert_200_and_items_equal(get_data(slideshow), response)


def test_detail_return_404_when_user_is_not_from_same_team(client):
    slideshow = SlideshowFactory()
    url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
    response = client.get(url)
    assert status.HTTP_404_NOT_FOUND == response.status_code


class AdminUserTests(object):

    def setUp(self):
        self.team = TeamFactory()
        self.user = UserFactory(is_staff=True, teams=[self.team])
        self.client.force_authenticate(user=self.user)
        self.tm_patcher = patch('rafee.slideshows.serializers.TemplateManager')
        self.tm_mock = self.tm_patcher.start()
        self.manager = self.tm_mock.return_value
        self.manager.template_exists.return_value = True


def test_list_returns_all_slideshows(admin_client, admin_user):
    team1 = TeamFactory()
    team2 = TeamFactory()
    team3 = TeamFactory()
    admin_user.teams.add(team3)
    slideshows = [
        get_data(SlideshowFactory(team=team1)),
        get_data(SlideshowFactory(team=team2)),
        get_data(SlideshowFactory(team=team3)),
    ]
    response = admin_client.get(reverse('slideshow-list'))
    assert_200_and_items_equal(slideshows, response)


def test_create(admin_client):
    with patch('rafee.slideshows.serializers.TemplateManager'):
        team = TeamFactory()
        payload = {
            'name': 'showmatch',
            'team': team.id,
            'templates': 'a,b',
            'transition_interval': 90,
            'caching_interval': 90,
        }
        response = admin_client.post(reverse('slideshow-list'), data=payload)
        slideshow = Slideshow.objects.get(pk=response.data['id'])
        assert_201_and_items_equal(get_data(slideshow), response)


@patch('rafee.slideshows.serializers.TemplateManager')
def test_create_returns_400_if_template_not_exists(tm_mock, admin_client):
    manager = tm_mock.return_value
    manager.template_exists.side_effect = [True, False]
    team = TeamFactory()
    templates = ['t/in', 't/not_in']
    payload = {
        'name': 'showmatch',
        'team': team.id,
        'templates': ','.join(templates),
    }
    response = admin_client.post(reverse('slideshow-list'), data=payload)
    expected = {'templates': [TEMPLATES_NOT_FOUND.format('t/not_in')]}
    assert_status_and_items_equal(
        status.HTTP_400_BAD_REQUEST,
        expected,
        response,
    )


def test_create_returns_400_if_missing_required_args(admin_client):
    response = admin_client.post(reverse('slideshow-list'), data={})
    assert_items_equal(['name', 'team', 'templates'], response.data.keys())


def test_create_allows_same_name_for_different_teams(admin_client):
    with patch('rafee.slideshows.serializers.TemplateManager'):
        name = 'same name'
        team1 = TeamFactory()
        SlideshowFactory(name=name, team=team1)
        team2 = TeamFactory()
        payload = {'name': name, 'team': team2.id, 'templates': 'a,b'}
        response = admin_client.post(reverse('slideshow-list'), data=payload)
        slideshow = Slideshow.objects.get(pk=response.data['id'])
        assert_201_and_items_equal(get_data(slideshow), response)


def test_create_returns_400_if_name_exists_for_same_team(admin_client):
    with patch('rafee.slideshows.serializers.TemplateManager'):
        name = 'same name'
        team = TeamFactory()
        SlideshowFactory(name=name, team=team)
        payload = {'name': name, 'team': team.id, 'templates': 'a,b'}
        response = admin_client.post(reverse('slideshow-list'), data=payload)
        assert_expected_duplicate_name(response)


def test_detail_admin(admin_client):
    slideshow = SlideshowFactory()
    url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
    response = admin_client.get(url)
    assert_200_and_items_equal(get_data(slideshow), response)


def test_update(admin_client):
    with patch('rafee.slideshows.serializers.TemplateManager'):
        team = TeamFactory()
        slideshow = SlideshowFactory()
        payload = {'name': 'new name', 'team': team.id, 'templates': '11,22'}
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = admin_client.put(url, data=payload)
        updated_slideshow = Slideshow.objects.get(id=slideshow.id)
        assert_200_and_items_equal(get_data(updated_slideshow), response)


def test_update_returns_400_if_missing_required_args(admin_client):
    slideshow = SlideshowFactory()
    url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
    response = admin_client.put(url, data={})
    assert_items_equal(['name', 'team', 'templates'], response.data.keys())


def test_update_returns_400_if_name_exists_for_same_team(admin_client):
    with patch('rafee.slideshows.serializers.TemplateManager'):
        name = 'same name'
        team = TeamFactory()
        SlideshowFactory(name=name, team=team)
        slideshow = SlideshowFactory(team=team)
        payload = {'name': name, 'team': team.id, 'templates': '11,22'}
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = admin_client.put(url, data=payload)
        assert_expected_duplicate_name(response)


def test_partial_update(admin_client):
    slideshow = SlideshowFactory(name='some name')
    payload = {'name': 'new name'}
    url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
    response = admin_client.patch(url, data=payload)
    updated_slideshow = Slideshow.objects.get(id=slideshow.id)
    assert_200_and_items_equal(
        get_data(updated_slideshow),
        response,
    )


def test_partial_update_returns_400_if_name_exist_for_team(admin_client):
    name = 'same name'
    team = TeamFactory()
    SlideshowFactory(name=name, team=team)
    slideshow = SlideshowFactory(team=team)
    payload = {'name': name}
    url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
    response = admin_client.patch(url, data=payload)
    assert_expected_duplicate_name(response)


def test_delete(admin_client):
    slideshow = SlideshowFactory()
    url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
    response = admin_client.delete(url)
    assert status.HTTP_204_NO_CONTENT == response.status_code
    assert response.data is None
    with pytest.raises(Slideshow.DoesNotExist):
        Slideshow.objects.get(id=slideshow.id)
