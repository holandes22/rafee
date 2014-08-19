import unittest


class GitManagerTests(unittest.TestCase):

    def test_clone_works_with_a_url(self):
        pass

    def test_clone_works_with_a_file_path(self):
        pass

    def test_clone_raises_if_failure(self):
        pass

    def test_pull_only_pulls_if_needed(self):
        # Fetch and only then pull
        pass

    def test_pull_raises_failure_if_unstaged_changes(self):
        pass

    def test_pull_raises_failure_if_unpushed_commits(self):
        pass
