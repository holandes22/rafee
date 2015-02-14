import pytest
from mock import patch
from celery import states

from rafee.templates.tasks import render

# pylint: disable=redefined-outer-name


@pytest.yield_fixture
def manager():
    with patch('rafee.templates.tasks.TemplateManager') as manager:
        yield manager.return_value


def test_render_with_no_data_source(manager):
    manager.get_template_info.return_value = {'data_source_url': None}
    template = 'fake'
    manager.render.return_value = template
    result = render.delay('some_template')
    assert template == result.result
    manager.render.assert_called_with('some_template', data_source={})


@patch('rafee.templates.tasks.requests')
def test_render_with_data_source(requests, manager):
    manager.get_template_info.return_value = {
        'data_source_url': 'url',
    }
    template = 'fake'
    manager.render.return_value = template
    result = render.delay('some_template')
    assert template == result.result
    requests.get.assert_called_with('url')


def test_task_includes_error(manager):
    error = ValueError()
    manager.get_template_info.side_effect = error
    result = render.delay('some_template')
    assert error == result.result
    assert states.FAILURE == result.status
