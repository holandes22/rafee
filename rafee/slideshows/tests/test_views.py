from django.core.urlresolvers import reverse

from rest_framework import status

from rafee.test_utils.data import get_data
from rafee.test_utils.base import BaseAPITestCase
from rafee.test_utils.base import CommonTestsMixin
from rafee.test_utils.base import NonAdminWriteTestsMixin

from rafee.teams.factories import TeamFactory
from rafee.users.factories import UserFactory
from rafee.slideshows.factories import SlideshowFactory

from rafee.slideshows.models import Slideshow


class CommonSlideshowTests(CommonTestsMixin, BaseAPITestCase):

    list_url_name = 'slideshow-list'
    detail_url_name = 'slideshow-detail'

    def setUp(self):
        self.slideshow = SlideshowFactory()
        self.detail_url_kwargs = {'id': self.slideshow.id}


class NonAdminSlideshowTests(NonAdminWriteTestsMixin, BaseAPITestCase):

    list_url_name = 'slideshow-list'
    detail_url_name = 'slideshow-detail'

    def setUp(self):
        self.team = TeamFactory()
        self.user = UserFactory(teams=[self.team])
        self.client.force_authenticate(user=self.user)
        self.slideshow = SlideshowFactory()
        self.detail_url_kwargs = {'id': self.slideshow.id}

    def test_list(self):
        slideshow = SlideshowFactory(team=self.team)
        self.assertResponse200AndItemsEqual(
            [get_data(slideshow)],
            self.client.get(reverse('slideshow-list'))
        )

    def test_list_returns_slideshows_from_the_user_team(self):
        my_slideshow = SlideshowFactory(team=self.team)
        SlideshowFactory()
        response = self.client.get(reverse('slideshow-list'))
        self.assertResponse200AndItemsEqual(
            [get_data(my_slideshow)],
            response,
        )

    def test_detail(self):
        slideshow = SlideshowFactory(team=self.team)
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(get_data(slideshow), response)

    def test_detail_return_404_when_user_is_not_from_same_team(self):
        slideshow = SlideshowFactory()
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class AdminUserTests(BaseAPITestCase):

    def setUp(self):
        self.team = TeamFactory()
        self.user = UserFactory(is_admin=True, teams=[self.team])
        self.client.force_authenticate(user=self.user)

    def assertExpectedDuplicateName(self, response):
        expected = {
            '__all__': ['Slideshow with this Name and Team already exists.'],
        }
        self.assertResponseStatusAndItemsEqual(
            status.HTTP_400_BAD_REQUEST,
            expected,
            response,
        )

    def test_list_returns_all_slideshows(self):
        team1 = TeamFactory()
        team2 = TeamFactory()
        slideshows = [
            get_data(SlideshowFactory(team=team1)),
            get_data(SlideshowFactory(team=team2)),
            get_data(SlideshowFactory(team=self.team)),
        ]
        response = self.client.get(reverse('slideshow-list'))
        self.assertResponse200AndItemsEqual(slideshows, response)

    def test_create(self):
        team = TeamFactory()
        payload = {
            'name': 'showmatch',
            'team': team.id,
            'templates': 'a,b',
            'transition_interval': 90,
            'caching_interval': 90,
        }
        response = self.client.post(reverse('slideshow-list'), data=payload)
        slideshow = Slideshow.objects.get(pk=response.data['id'])
        self.assertResponse201AndItemsEqual(get_data(slideshow), response)

    def test_create_returns_400_if_missing_required_args(self):
        response = self.client.post(reverse('slideshow-list'), data={})
        self.assertItemsEqual(
            ['name', 'team', 'templates'],
            response.data.keys(),
        )

    def test_create_allows_same_name_for_different_teams(self):
        name = 'same name'
        team1 = TeamFactory()
        SlideshowFactory(name=name, team=team1)
        team2 = TeamFactory()
        payload = {'name': name, 'team': team2.id, 'templates': 'a,b'}
        response = self.client.post(reverse('slideshow-list'), data=payload)
        slideshow = Slideshow.objects.get(pk=response.data['id'])
        self.assertResponse201AndItemsEqual(get_data(slideshow), response)

    def test_create_returns_400_if_name_exists_for_same_team(self):
        name = 'same name'
        team = TeamFactory()
        SlideshowFactory(name=name, team=team)
        payload = {'name': name, 'team': team.id, 'templates': 'a,b'}
        response = self.client.post(reverse('slideshow-list'), data=payload)
        self.assertExpectedDuplicateName(response)

    def test_detail(self):
        slideshow = SlideshowFactory()
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(get_data(slideshow), response)

    def test_update(self):
        team = TeamFactory()
        slideshow = SlideshowFactory()
        payload = {'name': 'new name', 'team': team.id, 'templates': '11,22'}
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = self.client.put(url, data=payload)
        updated_slideshow = Slideshow.objects.get(id=slideshow.id)
        self.assertResponse200AndItemsEqual(
            get_data(updated_slideshow),
            response,
        )

    def test_update_returns_400_if_missing_required_args(self):
        slideshow = SlideshowFactory()
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = self.client.put(url, data={})
        self.assertItemsEqual(
            ['name', 'team', 'templates'],
            response.data.keys(),
        )

    def test_update_returns_400_if_name_exists_for_same_team(self):
        name = 'same name'
        team = TeamFactory()
        SlideshowFactory(name=name, team=team)
        slideshow = SlideshowFactory(team=team)
        payload = {'name': name, 'team': team.id, 'templates': '11,22'}
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = self.client.put(url, data=payload)
        self.assertExpectedDuplicateName(response)

    def test_partial_update(self):
        slideshow = SlideshowFactory(name='some name')
        payload = {'name': 'new name'}
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = self.client.patch(url, data=payload)
        updated_slideshow = Slideshow.objects.get(id=slideshow.id)
        self.assertResponse200AndItemsEqual(
            get_data(updated_slideshow),
            response,
        )

    def test_partial_update_returns_400_if_name_exists_for_same_team(self):
        name = 'same name'
        team = TeamFactory()
        SlideshowFactory(name=name, team=team)
        slideshow = SlideshowFactory(team=team)
        payload = {'name': name}
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = self.client.patch(url, data=payload)
        self.assertExpectedDuplicateName(response)

    def test_delete(self):
        slideshow = SlideshowFactory()
        url = reverse('slideshow-detail', kwargs={'id': slideshow.id})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertIsNone(response.data)
        with self.assertRaises(Slideshow.DoesNotExist):
            Slideshow.objects.get(id=slideshow.id)
