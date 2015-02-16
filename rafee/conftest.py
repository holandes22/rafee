from contextlib import contextmanager

import pytest
from rest_framework.test import APIClient

from rafee.users.factories import UserFactory

# pylint: disable=redefined-outer-name,unused-argument,invalid-name


@contextmanager
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    yield client
    client.logout()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def admin_user(db):
    return UserFactory(is_staff=True)


@pytest.yield_fixture
def client(user):
    with api_client(user) as authenticated_client:
        yield authenticated_client


@pytest.yield_fixture
def admin_client(admin_user):
    with api_client(admin_user) as authenticated_client:
        yield authenticated_client


@pytest.fixture
def anon_client():
    return APIClient()
