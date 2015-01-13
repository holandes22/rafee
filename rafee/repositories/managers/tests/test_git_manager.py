import unittest
from mock import patch, Mock, PropertyMock
from git.exc import InvalidGitRepositoryError

from rafee.repositories.managers.git import GitManager
from rafee.repositories.managers.git import CannotPullFromRepoError


class GitManagerTests(unittest.TestCase):

    def setUp(self):
        self.url = 'http://fake'
        self.dst_path = '/fake/dst/path'
        self.os_patcher = patch('rafee.repositories.managers.git.os')
        self.git_patcher = patch('rafee.repositories.managers.git.git')
        self.clone_or_get_patcher = patch.object(
            GitManager,
            'clone_or_get_local_copy',
        )
        self.os_mock = self.os_patcher.start()
        self.git_mock = self.git_patcher.start()
        self.clone_or_get_mock = self.clone_or_get_patcher.start()
        self.git_manager = GitManager(self.url, self.dst_path)

    def tearDown(self):
        patchers = [
            self.os_patcher,
            self.git_patcher,
            self.clone_or_get_patcher,
        ]
        for patcher in patchers:
            try:
                patcher.stop()
            except RuntimeError:
                # patcher already stopped
                continue

    def test_clone(self):
        repo = Mock()
        self.git_mock.Repo.clone_from.return_value = repo
        response = self.git_manager.clone()
        self.assertEqual(repo, response)
        self.git_mock.Repo.clone_from.assert_called_with(
            self.url,
            self.dst_path,
        )

    def test_clone_creates_the_dir_if_needed(self):
        self.os_mock.path.exists.return_value = False
        self.git_manager.clone()
        self.os_mock.mkdir.assert_called_with(self.dst_path)

    @patch.object(GitManager, 'local_copy_exists', new_callable=PropertyMock)
    def test_clone_only_if_needed(self, local_copy_exists):
        local_copy_exists.return_value = False
        self.git_manager.clone()
        self.git_mock.Repo.clone_from.assert_called_with(
            self.url,
            self.dst_path,
        )

    def test_local_copy_exists(self):
        self.os_mock.path.exists.return_value = True
        self.assertTrue(self.git_manager.local_copy_exists)
        self.os_mock.path.exists.assert_called_with(self.dst_path)

    def test_is_valid_local_copy(self):
        remote = Mock()
        remote.url = self.url
        repo = Mock()
        repo.remote.return_value = remote
        self.git_mock.Repo.return_value = repo
        self.assertTrue(self.git_manager.is_valid_local_copy)

    def test_is_valid_local_returns_false_if_url_mismatch(self):
        fake_url = self.url + 'not_the_same'
        remote = Mock()
        remote.url = fake_url
        repo = Mock()
        repo.remote.return_value = remote
        self.git_mock.Repo.return_value = repo
        git_manager = GitManager(self.url, self.dst_path)
        self.assertFalse(git_manager.is_valid_local_copy)

    @patch.object(GitManager, 'clone')
    @patch.object(GitManager, 'local_copy_exists', new_callable=PropertyMock)
    def test_clone_or_get_clones_if_no_local_copy(self, local_copy, clone):
        self.clone_or_get_patcher.stop()
        local_copy.return_value = False
        self.git_manager.clone_or_get_local_copy()
        self.assertTrue(self.git_manager.clone.called)

    @patch.object(GitManager, 'is_valid_local_copy', new_callable=PropertyMock)
    def test_clone_or_get_returns_local_copy_if_valid_repo(self, valid_copy):
        self.clone_or_get_patcher.stop()
        valid_copy.return_value = True
        repo = Mock()
        self.git_mock.Repo.return_value = repo
        self.assertEqual(repo, self.git_manager.clone_or_get_local_copy())
        self.git_mock.Repo.assert_called_with(self.dst_path)
        self.assertFalse(self.git_mock.Repo.clone_from.called)

    @patch.object(GitManager, 'is_valid_local_copy', new_callable=PropertyMock)
    def test_clone_or_get_raises_error_if_not_a_valid_repo(self, valid_copy):
        self.clone_or_get_patcher.stop()
        valid_copy.return_value = False
        with self.assertRaises(InvalidGitRepositoryError):
            self.git_manager.clone_or_get_local_copy()

    def test_is_ahead_returns_true_if_new_commits(self):
        commits = [Mock(), Mock()]
        self.git_manager.repo.iter_commits.return_value = commits
        self.assertTrue(self.git_manager.is_ahead)

    def test_is_ahead_returns_false_if_no_new_commits(self):
        self.git_manager.repo.iter_commits.return_value = []
        self.assertFalse(self.git_manager.is_ahead)

    def test_is_behind_returns_true_if_new_commits(self):
        commits = [Mock(), Mock()]
        self.git_manager.repo.iter_commits.return_value = commits
        self.assertTrue(self.git_manager.is_behind)

    def test_is_behind_returns_false_if_no_new_commits(self):
        self.git_manager.repo.iter_commits.return_value = []
        self.assertFalse(self.git_manager.is_behind)

    def test_count_commits_call_fetch_before_counting(self):
        self.git_manager.count_commits(Mock())
        self.assertTrue(self.git_manager.remote.fetch.called)

    @patch.object(GitManager, 'in_master_branch', new_callable=PropertyMock)
    @patch.object(GitManager, 'is_ahead', new_callable=PropertyMock)
    def generic_test_is_ok_to_pull(self, is_ahead, in_master, opts={}):
        __test__ = False
        is_ahead.return_value = opts.get('is_ahead', False)
        in_master.return_value = opts.get('in_master', False)
        repo = Mock()
        repo.is_dirty.return_value = opts.get('is_dirty', False)
        self.git_manager.repo = repo
        expected = opts.get('expected', False)
        self.assertEqual(expected, self.git_manager.is_ok_to_pull)

    def test_is_ok_to_pull(self):
        opts = {'in_master': True, 'expected': True}
        self.generic_test_is_ok_to_pull(opts=opts)

    def test_is_ok_to_pull_returns_false_if_dirty(self):
        opts = {'in_master': True, 'is_dirty': True}
        self.generic_test_is_ok_to_pull(opts=opts)

    def test_is_ok_to_pull_returns_false_if_unpushed(self):
        opts = {'is_ahead': True, 'in_master': True}
        self.generic_test_is_ok_to_pull(opts=opts)

    def test_is_ok_to_pull_returns_false_if_not_on_master(self):
        opts = {'is_ahead': True}
        self.generic_test_is_ok_to_pull(opts=opts)

    @patch.object(GitManager, 'is_ok_to_pull')
    @patch.object(GitManager, 'is_behind', new_callable=PropertyMock)
    def test_pull_only_pulls_if_needed(self, is_behind, is_ok):
        is_behind.return_value = False
        self.git_manager.pull()
        self.assertFalse(self.git_manager.remote.pull.called)

    @patch.object(GitManager, 'is_ok_to_pull')
    @patch.object(GitManager, 'is_behind', new_callable=PropertyMock)
    def test_pull(self, is_behind, is_ok):
        is_behind.return_value = True
        self.git_manager.pull()
        self.assertTrue(self.git_manager.remote.pull.called)

    @patch.object(GitManager, 'is_ok_to_pull', new_callable=PropertyMock)
    def test_pull_raises_error_if_not_ok_to_pull(self, is_ok):
        is_ok.return_value = False
        with self.assertRaises(CannotPullFromRepoError):
            self.git_manager.pull()

    def test_in_master_branch_is_true_if_in_master(self):
        self.git_manager.repo.active_branch.name = 'master'
        self.assertTrue(self.git_manager.in_master_branch)

    def test_in_master_branch_if_false_if_not_in_master(self):
        self.git_manager.repo.active_branch.name = 'not_master'
        self.assertFalse(self.git_manager.in_master_branch)
