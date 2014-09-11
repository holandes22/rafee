from mock import patch
from django.core.urlresolvers import reverse

from rafee.test_utils.base import BaseAPITestCase


class TaskTests(BaseAPITestCase):

    def extra_setup(self):
        self.ar_patcher = patch('rafee.tasks.views.app.AsyncResult')
        self.ar_mock = self.ar_patcher.start()
        self.result = self.ar_mock.return_value

    def test_detail_pending_task(self):
        self.result.status = 'PENDING'
        self.result.ready.return_value = False
        expected = {'status': 'PENDING'}
        url = reverse('task-detail', kwargs={'task_id': 'aaa-b1b1'})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(expected, response)

    def test_detail_failed_task(self):
        self.result.status = 'FAILED'
        error = ValueError('message')
        tb = 'fake_tb\njahsjhaks'
        self.result.result = error
        self.result.traceback = tb
        self.result.ready.return_value = True
        self.result.failed.return_value = True
        expected = {'status': 'FAILED', 'error': str(error), 'traceback': tb}
        url = reverse('task-detail', kwargs={'task_id': 'aaa-b1b1'})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(expected, response)

    def test_detail_success_task(self):
        self.result.status = 'SUCCESS'
        self.result.result = 1
        self.result.ready.return_value = True
        self.result.failed.return_value = False
        expected = {'status': 'SUCCESS', 'result': 1}
        url = reverse('task-detail', kwargs={'task_id': 'aaa-b1b1'})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(expected, response)
