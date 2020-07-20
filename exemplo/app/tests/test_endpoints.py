from .api_test_case import APITestCase
from django.urls import reverse


class TestUser(APITestCase):
    endpoint = reverse('user-list')

    def test_requires_authentication(self):
        self.assertRequiresAuthentication(self.endpoint, method=self.GET)

