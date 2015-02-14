import pytest
from mock import patch
from celery import states
from django.core.urlresolvers import reverse

from rafee.test_utils.assert_helpers import assert_200_and_items_equal

# pylint: disable=invalid-name,redefined-outer-name

task_id = 'aa-11'


@pytest.yield_fixture
def result():
    with patch('rafee.tasks.views.app.AsyncResult') as AsyncResult:
        yield AsyncResult.return_value


def test_detail_pending_task(result, client):
    result.status = states.PENDING
    result.ready.return_value = False
    expected = {'id': task_id, 'status': states.PENDING}
    url = reverse('task-detail', kwargs={'task_id': task_id})
    response = client.get(url)
    assert_200_and_items_equal(expected, response)


def test_detail_failed_task(result, client):
    result.status = states.FAILURE
    error = ValueError('message')
    traceback = 'fake_tb\njahsjhaks'
    result.result = error
    result.traceback = traceback
    result.ready.return_value = True
    result.failed.return_value = True
    expected = {
        'id': task_id,
        'status': states.FAILURE,
        'result': str(error),
        'traceback': traceback,
    }
    url = reverse('task-detail', kwargs={'task_id': task_id})
    response = client.get(url)
    assert_200_and_items_equal(expected, response)


def test_detail_success_task(result, client):
    result.status = states.SUCCESS
    result.result = 1
    result.ready.return_value = True
    result.failed.return_value = False
    expected = {'id': task_id, 'status': states.SUCCESS, 'result': 1}
    url = reverse('task-detail', kwargs={'task_id': task_id})
    response = client.get(url)
    assert_200_and_items_equal(expected, response)
