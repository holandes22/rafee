from mock import patch
from django.core.urlresolvers import reverse

from rafee.test_utils.base import BaseAPITestCase
from rafee.test_utils.base import CommonListTestsMixin
from rafee.test_utils.base import NonAdminListReadTestsMixin

from rafee.users.factories import UserFactory


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
