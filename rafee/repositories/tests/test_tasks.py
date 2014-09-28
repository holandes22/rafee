from mock import patch, Mock
from celery import states
from django.test import TestCase

from rafee.repositories.models import Repository
from rafee.repositories.factories import RepositoryFactory
from rafee.repositories.tasks import clone_and_create_repo
from rafee.repositories.tasks import pull_repo, pull_all_repos


class RepositoryTasksTests(TestCase):

    def setUp(self):
        self.gm_patcher = patch('rafee.repositories.tasks.GitManager')
        self.gm_mock = self.gm_patcher.start()

    def tearDown(self):
        self.gm_patcher.stop()

    def test_task_includes_error(self):
        error = IOError('Cannot clone there')
        self.gm_mock.side_effect = error
        result = clone_and_create_repo.delay('http://some.url/fake')
        self.assertEqual(error, result.result)
        self.assertEqual(states.FAILURE, result.status)

    @patch('rafee.repositories.tasks.get_dst_path')
    def test_clone_and_create(self, get_dst_path):
        url = 'http://some.url/fake'
        get_dst_path.return_value = 'fake'
        result = clone_and_create_repo.delay(url)
        self.gm_mock.assert_called_with(url, 'fake')
        repo = Repository.objects.get(id=result.result)
        self.assertEqual(url, repo.url)

    def test_clone_and_create_removes_git_extension_from_folder(self):
        url = 'http://some.url/fake.git'
        result = clone_and_create_repo.delay(url)
        self.gm_mock.assert_called_with(url, 'fake')

    @patch('rafee.repositories.tasks.get_dst_path')
    def test_pull_all_repos(self, get_dst_path):
        git_manager = self.gm_mock.return_value
        RepositoryFactory()
        RepositoryFactory()
        result = pull_all_repos.delay()
        self.assertListEqual([], result.result['errors'])
        self.assertEqual(2, git_manager.pull.call_count)

    @patch('rafee.repositories.tasks.get_dst_path')
    def test_pull_all_repos_return_error_info(self, get_dst_path):
        git_manager = self.gm_mock.return_value
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
        self.assertEqual(expected, result.result['errors'])

    @patch('rafee.repositories.tasks.get_dst_path')
    def test_pull_repo(self, get_dst_path):
        git_manager = self.gm_mock.return_value
        url = 'http://some.url/fake'
        get_dst_path.return_value = 'fake'
        result = pull_repo.delay(url)
        self.assertIsNone(result.result)
        self.gm_mock.assert_called_with(url, 'fake')
        git_manager.pull.assert_called_with()
