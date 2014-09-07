from nose.tools import nottest
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from rafee.users.factories import UserFactory


class BaseAPITestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def assertResponseStatusAndItemsEqual(self, code, expected, response):
        actual = response.data
        self.assertEqual(code, response.status_code)
        self.assertItemsEqual(expected, actual)

    def assertResponse200AndItemsEqual(self, expected, response):
        self.assertResponseStatusAndItemsEqual(
            status.HTTP_200_OK,
            expected,
            response,
        )

    def assertResponse201AndItemsEqual(self, expected, response):
        self.assertResponseStatusAndItemsEqual(
            status.HTTP_201_CREATED,
            expected,
            response,
        )

    @nottest
    def generic_test_list_returns_status_code(self, method, status_code):
        url = reverse(self.list_url_name)
        response = getattr(self.client, method)(url)
        self.assertEqual(status_code, response.status_code)

    @nottest
    def generic_test_detail_returns_status_code(self, method, status_code):
        url = reverse(self.detail_url_name, kwargs=self.detail_url_kwargs)
        response = getattr(self.client, method)(url)
        self.assertEqual(status_code, response.status_code)

    @nottest
    def generic_test_list_returns_401_if_not_authenticated(self, method):
        self.generic_test_list_returns_status_code(
            method,
            status.HTTP_401_UNAUTHORIZED,
        )

    @nottest
    def generic_test_detail_returns_401_if_not_authenticated(self, method):
        self.generic_test_detail_returns_status_code(
            method,
            status.HTTP_401_UNAUTHORIZED,
        )

    @nottest
    def generic_test_list_returns_405_if_method_not_allowed(self, method):
        # We just want to test 405, so we avoid permissions by using
        # a user who'll probably has all acces
        user = UserFactory(is_admin=True)
        self.client.force_authenticate(user=user)
        self.generic_test_list_returns_status_code(
            method,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @nottest
    def generic_test_detail_returns_405_if_method_not_allowed(self, method):
        user = UserFactory(is_admin=True)
        self.client.force_authenticate(user=user)
        self.generic_test_detail_returns_status_code(
            method,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @nottest
    def generic_test_list_method_returns_403(self, method):
        self.generic_test_list_returns_status_code(
            method,
            status.HTTP_403_FORBIDDEN,
        )

    @nottest
    def generic_test_detail_method_returns_403(self, method):
        self.generic_test_detail_returns_status_code(
            method,
            status.HTTP_403_FORBIDDEN,
        )


class CommonTestsMixin(object):

    # authenticated list tests
    def test_list_get_returns_401_if_not_authenticated(self):
        self.generic_test_list_returns_401_if_not_authenticated('get')

    def test_list_post_returns_401_if_not_authenticated(self):
        self.generic_test_list_returns_401_if_not_authenticated('post')

    # authenticated detail tests
    def test_detail_get_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('get')

    def test_detail_post_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('post')

    def test_detail_put_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('put')

    def test_detail_patch_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('patch')

    def test_detail_delete_returns_401_if_not_authenticated(self):
        self.generic_test_detail_returns_401_if_not_authenticated('delete')

    # allowed list tests
    def test_list_put_returns_405(self):
        self.generic_test_list_returns_405_if_method_not_allowed('put')

    def test_list_patch_returns_405(self):
        self.generic_test_list_returns_405_if_method_not_allowed('patch')

    def test_list_delete_returns_405(self):
        self.generic_test_list_returns_405_if_method_not_allowed('delete')

    # allowed detail tests
    def test_detail_post_returns_405(self):
        self.generic_test_detail_returns_405_if_method_not_allowed('post')


class NonAdminListReadTestsMixin(object):

    def test_list_get_returns_403(self):
        self.generic_test_list_method_returns_403('get')


class NonAdminDetailReadTestsMixin(object):

    def test_detail_get_returns_403(self):
        self.generic_test_detail_method_returns_403('get')


class NonAdminReadTestsMixin(NonAdminListReadTestsMixin,
                             NonAdminDetailReadTestsMixin):
    pass


class NonAdminListWriteTestsMixin(object):

    def test_list_post_returns_403(self):
        self.generic_test_list_method_returns_403('post')


class NonAdminDetailWriteTestsMixin(object):

    def test_update_returns_403(self):
        self.generic_test_detail_method_returns_403('put')

    def test_partial_update_returns_403(self):
        self.generic_test_detail_method_returns_403('patch')

    def test_delete_returns_403(self):
        self.generic_test_detail_method_returns_403('delete')


class NonAdminWriteTestsMixin(NonAdminListWriteTestsMixin,
                              NonAdminDetailWriteTestsMixin):
    pass
