from django.test import TestCase

from rafee.users.factories import UserFactory


class UserModelTests(TestCase):

    def test_get_short_name_returns_email(self):
        email = 'pp@pp.com'
        user = UserFactory(email=email)
        self.assertEqual(email, user.get_short_name())
