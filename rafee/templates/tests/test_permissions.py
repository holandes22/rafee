import pytest
from mock import Mock

from rafee.users.factories import UserFactory
from rafee.teams.factories import TeamFactory
from rafee.slideshows.factories import SlideshowFactory
from rafee.templates.permissions import IsAllowedToSeeTemplate

# pylint: disable=invalid-name


@pytest.mark.django_db
def test_returns_true_if_staff_member():
    request = Mock()
    request.user = UserFactory(is_staff=True, is_superuser=False)
    permission = IsAllowedToSeeTemplate()
    assert permission.has_permission(request, Mock())


@pytest.mark.django_db
def test_returns_true_if_missing_template_name():
    request = Mock()
    request.user = UserFactory(is_staff=False, is_superuser=False)
    request.data.get.return_value = None
    permission = IsAllowedToSeeTemplate()
    assert permission.has_permission(request, Mock())


@pytest.mark.django_db
def test_returns_true_if_belongs_to_one_of_its_slideshows():
    team1 = TeamFactory()
    team2 = TeamFactory()
    SlideshowFactory(templates='repo/t,repo1/t', team=team1)
    request = Mock()
    request.user = UserFactory(teams=[team1, team2])
    request.data.get.return_value = 'repo/t'
    permission = IsAllowedToSeeTemplate()
    assert permission.has_permission(request, Mock())


@pytest.mark.django_db
def test_returns_false_if_not_in_its_slideshows():
    team = TeamFactory()
    SlideshowFactory(templates='repo/t,repo1/t', team=team)
    request = Mock()
    request.user = UserFactory()
    permission = IsAllowedToSeeTemplate()
    assert not permission.has_permission(request, Mock())
