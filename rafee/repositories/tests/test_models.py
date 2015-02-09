import pytest
from django.db import IntegrityError

from rafee.repositories.models import Repository


@pytest.mark.django_db
def test_create_raises_validation_error_if_url_not_unique():
    same_url = 'http://1'
    Repository.objects.create(url=same_url)
    with pytest.raises(IntegrityError) as excinfo:
        Repository.objects.create(url=same_url)
    assert 'url' in str(excinfo.value)
