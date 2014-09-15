from mock import patch
from django.core.urlresolvers import reverse
from rest_framework import status

from rafee.test_utils.base import BaseAPITestCase
from rafee.test_utils.base import CommonListTestsMixin
from rafee.test_utils.base import NonAdminListReadTestsMixin
from rafee.users.factories import UserFactory
from rafee.teams.factories import TeamFactory
from rafee.slideshows.factories import SlideshowFactory


class CommonTemplateTests(CommonListTestsMixin, BaseAPITestCase):

    list_url_name = 'template-list'


class NonAdminTemplateTests(NonAdminListReadTestsMixin, BaseAPITestCase):

    list_url_name = 'template-list'


class AdminTemplateTests(BaseAPITestCase):

    def setUp(self):
        self.user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=self.user)

    @patch('rafee.templates.views.TemplateManager')
    def test_list(self, TemplateManager_m):
        manager = TemplateManager_m.return_value
        fake_info = [
            {'name': 'repo1/t', 'data_source_url': 'http://url1.com/t'},
            {'name': 'repo2/t', 'data_source_url': None},
        ]
        manager.get_templates_info.return_value = fake_info
        response = self.client.get(reverse('template-list'))
        self.assertResponse200AndItemsEqual(fake_info, response)


class TemplateRenderTests(BaseAPITestCase):

    def setUp(self):
        self.team1 = TeamFactory()
        self.team2 = TeamFactory()
        self.user = UserFactory(teams=[self.team1, self.team2])
        SlideshowFactory(templates='repo/t,repo1/t', team=self.team1)
        self.client.force_authenticate(user=self.user)

    @patch('rafee.templates.tasks.requests')
    @patch('rafee.templates.tasks.TemplateManager')
    def test_render(self, TemplateManager_m, requests_m):
        manager = TemplateManager_m.return_value
        manager.render.return_value = 'Rendered template!'
        payload = {'template_name': 'repo/t'}
        response = self.client.post(reverse('template-render'), data=payload)
        self.assertIn('task', response.data)

    def test_render_returns_400_if_no_template_name(self):
        response = self.client.post(reverse('template-render'), data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn('template_name', response.data)

    def test_render_returns_403_if_user_has_no_access_to_template(self):
        payload = {'template_name': 'repo/fake'}
        response = self.client.post(reverse('template-render'), data=payload)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_render_allows_admin_to_render_any_template(self):
        user = UserFactory(is_staff=True)
        self.client.force_authenticate(user=user)
        payload = {'template_name': 'repo/fake'}
        response = self.client.post(reverse('template-render'), data=payload)
        self.assertIn('task', response.data)
