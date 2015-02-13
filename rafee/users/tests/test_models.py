import pytest
from rafee.users.factories import UserFactory

@pytest.mark.django_db
def test_get_short_name_returns_email():
    email = 'pp@pp.com'
    user = UserFactory(email=email)
    assert email == user.get_short_name()
