import pytest
from rest_framework.test import APIClient

from rafee.users.factories import UserFactory


@pytest.fixture()
def user(db):
    return UserFactory()


@pytest.fixture()
def admin_user(db):
    return UserFactory(is_staff=True)


@pytest.yield_fixture()
def client(user):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.logout()


@pytest.yield_fixture()
def admin_client(admin_user):
    api_client = APIClient()
    api_client.force_authenticate(user=admin_user)
    yield api_client
    api_client.logout()


@pytest.fixture()
def anon_client():
    return APIClient()
