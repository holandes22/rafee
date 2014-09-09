from django.test import TestCase
from django.db import IntegrityError

from rafee.repositories.models import Repository


class RepositoryModelTests(TestCase):

    def test_create_raises_validation_error_if_url_not_unique(self):
        same_url = 'http://1'
        repo1 = Repository(url=same_url)
        repo2 = Repository(url=same_url)
        repo1.save()
        with self.assertRaises(IntegrityError) as ctx:
            repo2.save()
            self.assertTrue('url' in str(ctx.exception))
