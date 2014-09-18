from mock import patch
from celery import states
from django.test import TestCase

from rafee.templates.tasks import render


class TemplatesTasksTests(TestCase):

    def setUp(self):
        self.tm_patcher = patch('rafee.templates.tasks.TemplateManager')
        self.TemplateManager_mock = self.tm_patcher.start()
        self.manager = self.TemplateManager_mock.return_value

    def tearDown(self):
        self.tm_patcher.stop()

    def test_render_with_no_data_source(self):
        self.manager.get_template_info.return_value = {'data_source_url': None}
        template = 'fake'
        self.manager.render.return_value = template
        result = render.delay('some_template')
        self.assertEqual(template, result.result)
        self.manager.render.assert_called_with('some_template', data_source={})

    @patch('rafee.templates.tasks.requests')
    def test_render_with_data_source(self, requests_m):
        self.manager.get_template_info.return_value = {
            'data_source_url': 'url',
        }
        template = 'fake'
        self.manager.render.return_value = template
        result = render.delay('some_template')
        self.assertEqual(template, result.result)
        requests_m.get.assert_called_with('url')

    def test_task_includes_error(self):
        error = ValueError()
        self.manager.get_template_info.side_effect = error
        result = render.delay('some_template')
        self.assertEqual(error, result.result)
        self.assertEqual(states.FAILURE, result.status)
