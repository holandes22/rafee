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
