from django.test import TestCase
from django.db import IntegrityError

from rafee.repositories.models import Repository


class RepositoryModelTests(TestCase):

    def test_create_raises_validation_error_if_url_not_unique(self):
        same_url = 'http://1'
        Repository.objects.create(url=same_url)
        with self.assertRaises(IntegrityError) as ctx:
            Repository.objects.create(url=same_url)
            self.assertTrue('url' in str(ctx.exception))
