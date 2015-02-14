import json

from mock import patch, Mock
from django.core.urlresolvers import reverse
from rest_framework import status

from rafee.test_utils.assert_helpers import assert_status_and_items_equal
from rafee.test_utils.assert_helpers import assert_200_and_items_equal
from rafee.messages import TEMPLATE_NOT_FOUND
from rafee.users.factories import UserFactory
from rafee.teams.factories import TeamFactory
from rafee.slideshows.factories import SlideshowFactory


@patch('rafee.templates.views.TemplateManager')
def test_list(tm_mock, admin_client):
    manager = tm_mock.return_value
    fake_info = [
        {'name': 'repo1/t', 'data_source_url': 'http://url1.com/t'},
        {'name': 'repo2/t', 'data_source_url': None},
    ]
    manager.get_templates_info.return_value = fake_info
    response = admin_client.get(reverse('template-list'))
    assert_200_and_items_equal(fake_info, response)


@patch('rafee.templates.views.TemplateManager')
def test_render(tm_mock, user, client):
    with patch('rafee.templates.tasks.requests'):
        manager = tm_mock.return_value
        manager.render.return_value = 'Rendered template!'
        team = TeamFactory()
        user.teams.add(team)
        SlideshowFactory(templates='repo/t,repo1/t', team=team)
        payload = {'template_name': 'repo/t'}
        response = client.post(reverse('template-render'), data=payload)
        assert 'task' in response.data


def test_render_returns_400_if_no_template_name(client):
    response = client.post(reverse('template-render'), data={})
    assert status.HTTP_400_BAD_REQUEST == response.status_code
    assert 'template_name' in response.data


@patch('rafee.templates.views.TemplateManager')
def test_render_returns_500_if_non_existing_template(tm_mock, user, client):
    manager = tm_mock.return_value
    manager.template_exists.return_value = False
    team = TeamFactory()
    user.teams.add(team)
    SlideshowFactory(templates='repo/t,repo1/t', team=team)
    payload = {'template_name': 'repo/t'}
    response = client.post(reverse('template-render'), data=payload)
    assert_status_and_items_equal(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        expected={'detail': TEMPLATE_NOT_FOUND},
        response=response,
    )


def test_render_returns_403_if_user_has_no_access_to_template(client):
    team1 = TeamFactory()
    team2 = TeamFactory()
    UserFactory(teams=[team1, team2])
    payload = {'template_name': 'repo/fake'}
    response = client.post(reverse('template-render'), data=payload)
    assert status.HTTP_403_FORBIDDEN == response.status_code


@patch('rafee.templates.views.TemplateManager')
def test_render_allows_admin_to_render_any_template(tm_mock, admin_client):
    user = UserFactory(teams=[TeamFactory()])
    payload = {'template_name': 'repo/fake'}
    response = admin_client.post(reverse('template-render'), data=payload)
    assert 'task' in response.data


@patch('rafee.templates.views.TemplateManager')
def test_preview(tm_mock, client):
    template = 'Fake template'
    manager = tm_mock.return_value
    manager.render_from_string.return_value = template
    payload = {'template_str': template}
    response = client.post(reverse('template-preview'), data=payload)
    expected = {'preview': template}
    assert_200_and_items_equal(expected, response)


def test_preview_returns_400_if_no_template_str(client):
    response = client.post(reverse('template-preview'), data={})
    assert status.HTTP_400_BAD_REQUEST == response.status_code
    assert 'template_str' in response.data


@patch('rafee.templates.views.requests')
@patch('rafee.templates.views.TemplateManager')
def test_preview_fetches_data_source_url(tm_mock, requests_m, client):
    template = 'Fake template'
    manager = tm_mock.return_value
    manager.render_from_string.return_value = template
    url = 'http://blah.com/data.json'
    fake_json = json.dumps({'blah': 'blah'})
    json_mock = Mock()
    json_mock.json.return_value = fake_json
    requests_m.get.return_value = json_mock
    payload = {'template_str': template, 'data_source_url': url}
    response = client.post(reverse('template-preview'), data=payload)
    expected = {'preview': template}
    assert_200_and_items_equal(expected, response)
    requests_m.get.assert_called_with(url)
    manager.render_from_string.assert_called_with(
        template,
        data_source=fake_json,
    )


def test_preview_returns_403_if_user_has_no_access_to_included_template():
    # TODO: Avoid a permission boundary bug
    pass


def test_preview_returns_500_if_fetch_data_src_fails():
    # TODO: write
    pass
