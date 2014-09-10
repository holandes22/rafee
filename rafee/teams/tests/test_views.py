from django.core.urlresolvers import reverse

from rest_framework import status

from rafee.test_utils.data import get_data
from rafee.test_utils.base import BaseAPITestCase
from rafee.test_utils.base import CommonTestsMixin
from rafee.test_utils.base import NonAdminReadTestsMixin
from rafee.test_utils.base import NonAdminWriteTestsMixin

from rafee.teams.factories import TeamFactory
from rafee.users.factories import UserFactory

from rafee.teams.models import Team


class CommonTeamTests(CommonTestsMixin, BaseAPITestCase):

    list_url_name = 'team-list'
    detail_url_name = 'team-detail'

    def setUp(self):
        self.team = TeamFactory()
        self.detail_url_kwargs = {'id': self.team.id}


class NonAdminTeamTests(NonAdminReadTestsMixin,
                        NonAdminWriteTestsMixin,
                        BaseAPITestCase):

    list_url_name = 'team-list'
    detail_url_name = 'team-detail'

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.team = TeamFactory()
        self.detail_url_kwargs = {'id': self.team.id}


class AdminUserTests(BaseAPITestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        team = TeamFactory()
        response = self.client.get(reverse('team-list'))
        self.assertResponse200AndItemsEqual(
            [get_data(team)],
            response,
        )

    def test_list_teams_with_users(self):
        team = TeamFactory()
        user1 = UserFactory(teams=[team])
        user2 = UserFactory(teams=[team])
        response = self.client.get(reverse('team-list'))
        self.assertResponse200AndItemsEqual([get_data(team)], response)
        self.assertItemsEqual(
            [user1.id, user2.id],
            response.data[0]['users']
        )

    def test_create(self):
        payload = {'name': 'The A team'}
        response = self.client.post(reverse('team-list'), data=payload)
        team = Team.objects.get(pk=response.data['id'])
        self.assertResponse201AndItemsEqual(get_data(team), response)

    def test_detail(self):
        team = TeamFactory()
        UserFactory(teams=[team])
        url = reverse('team-detail', kwargs={'id': team.id})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(get_data(team), response)

    def test_update(self):
        team = TeamFactory(name='old name')
        UserFactory(teams=[team])
        payload = {'name': 'new name'}
        url = reverse('team-detail', kwargs={'id': team.id})
        response = self.client.put(url, data=payload)
        updated_team = Team.objects.get(id=team.id)
        self.assertResponse200AndItemsEqual(get_data(updated_team), response)

    def test_update_team_users(self):
        team = TeamFactory(name='old name')
        UserFactory(teams=[team])
        new_user = UserFactory()
        payload = {'name': 'new name', 'users': [new_user.id]}
        url = reverse('team-detail', kwargs={'id': team.id})
        self.client.put(url, data=payload)
        updated_team = Team.objects.get(id=team.id)
        self.assertEqual(new_user.username, updated_team.users.all()[0].username)

    def test_partial_update(self):
        team = TeamFactory(name='old name')
        payload = {'name': 'new name'}
        url = reverse('team-detail', kwargs={'id': team.id})
        response = self.client.patch(url, data=payload)
        updated_team = Team.objects.get(id=team.id)
        self.assertResponse200AndItemsEqual(get_data(updated_team), response)

    def test_delete(self):
        team = TeamFactory()
        url = reverse('team-detail', kwargs={'id': team.id})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertIsNone(response.data)
        with self.assertRaises(Team.DoesNotExist):
            Team.objects.get(id=team.id)
