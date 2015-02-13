import os

import pytest
from celery import states
from mock import patch, Mock
from django.conf import settings

from rafee.repositories.models import Repository
from rafee.repositories.factories import RepositoryFactory
from rafee.repositories.tasks import clone_and_create_repo
from rafee.repositories.tasks import pull_repo, pull_all_repos


# pylint: disable=invalid-name,redefined-outer-name


@pytest.yield_fixture
def gm_mock():
    gm_patcher = patch('rafee.repositories.tasks.GitManager')
    yield gm_patcher.start()
    gm_patcher.stop()


def test_task_includes_error(gm_mock):
    error = IOError('Cannot clone there')
    gm_mock.side_effect = error
    result = clone_and_create_repo.delay('http://some.url/fake')
    assert error == result.result
    assert states.FAILURE == result.status


@pytest.mark.django_db
@patch('rafee.repositories.tasks.get_dst_path')
def test_clone_and_create(get_dst_path, gm_mock):
    url = 'http://some.url/fake'
    get_dst_path.return_value = 'fake'
    result = clone_and_create_repo.delay(url)
    gm_mock.assert_called_with(url, 'fake')
    repo = Repository.objects.get(id=result.result)
    assert url == repo.url


def test_clone_and_create_removes_git_extension_from_folder(gm_mock):
    url = 'http://some.url/fake.git'
    clone_and_create_repo.delay(url)
    path = os.path.join(settings.RAFEE_REPO_DIR, 'fake')
    gm_mock.assert_called_with(url, path)


@pytest.mark.django_db
def test_pull_all_repos(gm_mock):
    with patch('rafee.repositories.tasks.get_dst_path'):
        git_manager = gm_mock.return_value
        RepositoryFactory()
        RepositoryFactory()
        result = pull_all_repos.delay()
        assert [] == result.result['errors']
        assert 2 == git_manager.pull.call_count


@pytest.mark.django_db
def test_pull_all_repos_return_error_info(gm_mock):
    with patch('rafee.repositories.tasks.get_dst_path'):
        git_manager = gm_mock.return_value
        RepositoryFactory()
        repo2 = RepositoryFactory()
        repo3 = RepositoryFactory()
        error2 = ValueError('Fake msg2')
        error3 = IOError()
        git_manager.pull.side_effect = [Mock(), error2, error3]
        result = pull_all_repos.delay()
        expected = [
            {'repo': repo2.id, 'message': str(error2), 'error': 'ValueError'},
            {'repo': repo3.id, 'message': str(error3), 'error': 'IOError'},
        ]
        assert expected == result.result['errors']


@patch('rafee.repositories.tasks.get_dst_path')
def test_pull_repo(get_dst_path, gm_mock):
    git_manager = gm_mock.return_value
    url = 'http://some.url/fake'
    get_dst_path.return_value = 'fake'
    result = pull_repo.delay(url)
    assert result.result is None
    gm_mock.assert_called_with(url, 'fake')
    git_manager.pull.assert_called_with()
