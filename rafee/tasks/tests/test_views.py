from mock import patch
from celery import states
from django.core.urlresolvers import reverse

from rafee.test_utils.base import BaseAPITestCase


class TaskTests(BaseAPITestCase):

    def extra_setup(self):
        # pylint: disable=attribute-defined-outside-init
        self.ar_patcher = patch('rafee.tasks.views.app.AsyncResult')
        self.ar_mock = self.ar_patcher.start()
        self.result = self.ar_mock.return_value
        self.task_id = 'aaa-b1b1'

    def test_detail_pending_task(self):
        self.result.status = states.PENDING
        self.result.ready.return_value = False
        expected = {'id': self.task_id, 'status': states.PENDING}
        url = reverse('task-detail', kwargs={'task_id': self.task_id})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(expected, response)

    def test_detail_failed_task(self):
        self.result.status = states.FAILURE
        error = ValueError('message')
        traceback = 'fake_tb\njahsjhaks'
        self.result.result = error
        self.result.traceback = traceback
        self.result.ready.return_value = True
        self.result.failed.return_value = True
        expected = {
            'id': self.task_id,
            'status': states.FAILURE,
            'result': str(error),
            'traceback': traceback,
        }
        url = reverse('task-detail', kwargs={'task_id': self.task_id})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(expected, response)

    def test_detail_success_task(self):
        self.result.status = states.SUCCESS
        self.result.result = 1
        self.result.ready.return_value = True
        self.result.failed.return_value = False
        expected = {'id': self.task_id, 'status': states.SUCCESS, 'result': 1}
        url = reverse('task-detail', kwargs={'task_id': self.task_id})
        response = self.client.get(url)
        self.assertResponse200AndItemsEqual(expected, response)
