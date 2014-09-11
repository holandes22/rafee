from mock import patch
from celery import states
from django.test import TestCase

from rafee.repositories.models import Repository
from rafee.repositories.tasks import clone_and_create_repo, pull_repo


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

    def test_a_scheduled_task_for_pulling_is_created_for_each_new_repo(self):
        pass

    @patch('rafee.repositories.tasks.get_dst_path')
    def test_pull_repo(self, get_dst_path):
        git_manager = self.gm_mock.return_value
        url = 'http://some.url/fake'
        get_dst_path.return_value = 'fake'
        result = pull_repo.delay(url)
        self.assertIsNone(result.result)
        self.gm_mock.assert_called_with(url, 'fake')
        git_manager.pull.assert_called_with()
