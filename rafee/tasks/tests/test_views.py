from mock import patch, Mock
from django.core.urlresolvers import reverse

from rafee.test_utils.base import BaseAPITestCase


class TaskTests(BaseAPITestCase):

    @patch('rafee.tasks.views.app.AsyncResult')
    def test_detail_pending_task(self, app_mock):
        result = app_mock.return_value
        result.status = 'PENDING'
        result.ready.return_value = False
        #app_mock.AsyncResult.return_value = result
        expected = {'status': 'PENDING'}
        url = reverse('task-detail', kwargs={'task_id': 'aaa-b1b1'})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(expected, response)

    @patch('rafee.tasks.views.app')
    def test_detail_failed_task(self, app_mock):
        result = Mock()
        result.status = 'FAILED'
        error = ValueError('message')
        tb = 'fake_tb\njahsjhaks'
        result.result = error
        result.traceback = tb
        result.ready.return_value = True
        result.failed.return_value = True
        app_mock.AsyncResult.return_value = result
        expected = {'status': 'FAILED', 'error': str(error), 'traceback': tb}
        url = reverse('task-detail', kwargs={'task_id': 'aaa-b1b1'})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(expected, response)

    @patch('rafee.tasks.views.app')
    def test_detail_success_task(self, app_mock):
        result = Mock()
        result.status = 'SUCCESS'
        result.result = 1
        result.ready.return_value = True
        result.failed.return_value = False
        app_mock.AsyncResult.return_value = result
        expected = {'status': 'SUCCESS', 'result': 1}
        url = reverse('task-detail', kwargs={'task_id': 'aaa-b1b1'})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(expected, response)
