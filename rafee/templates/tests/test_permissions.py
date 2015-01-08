from mock import Mock
from django.test import TestCase

from rafee.users.factories import UserFactory
from rafee.teams.factories import TeamFactory
from rafee.slideshows.factories import SlideshowFactory
from rafee.templates.permissions import IsAllowedToSeeTemplate


class TemplateAccessPermissionTests(TestCase):

    def setUp(self):
        self.permission = IsAllowedToSeeTemplate()

    def test_returns_true_if_staff_member(self):
        request = Mock()
        request.user = UserFactory(is_staff=True, is_superuser=False)
        self.assertTrue(
            self.permission.has_permission(request, Mock())
        )

    def test_returns_true_if_missing_template_name(self):
        request = Mock()
        request.user = UserFactory(is_staff=False, is_superuser=False)
        request.data.get.return_value = None
        self.assertTrue(
            self.permission.has_permission(request, Mock())
        )

    def test_returns_true_if_belongs_to_one_of_its_slideshows(self):
        team1 = TeamFactory()
        team2 = TeamFactory()
        SlideshowFactory(templates='repo/t,repo1/t', team=team1)
        request = Mock()
        request.user = UserFactory(teams=[team1, team2])
        request.data.get.return_value = 'repo/t'
        self.assertTrue(
            self.permission.has_permission(request, Mock())
        )

    def test_returns_false_if_not_in_its_slideshows(self):
        team = TeamFactory()
        SlideshowFactory(templates='repo/t,repo1/t', team=team)
        request = Mock()
        request.user = UserFactory()
        self.assertFalse(
            self.permission.has_permission(request, Mock())
        )
