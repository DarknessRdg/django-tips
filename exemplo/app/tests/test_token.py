from rest_framework_simplejwt.utils import datetime_from_epoch

from .api_test_case import APITestCase
from django.urls import reverse
from rest_framework_simplejwt import settings
from app.tokens import TokenDoisDiasAccess, TokenDoisDiasSerializer
import datetime


class TestTokenWithDifferentDuration(APITestCase):
    @property
    def data(self):
        return {
            'username': self.username,
            'password': self.password
        }

    def test_login(self):
        endpoint = reverse('login')
        response = self.client.post(endpoint, self.data)
        self.assertSuccess(response)

    def test_token_serializer(self):
        serializer = TokenDoisDiasSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        self.assertIn('access', serializer.validated_data)

    def test_pass_view_authentication(self):
        serializer = TokenDoisDiasSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['access']

        auth_endpoint = reverse('user-list')
        response = self.client.get(auth_endpoint, HTTP_AUTHORIZATION=f'JWT {token}')
        self.assertSuccess(response)

    def test_time(self):
        token = TokenDoisDiasAccess.for_user(self.user)

        token_duration = datetime_from_epoch(token['exp'])
        today = datetime.datetime.now()

        limit_day = today.day + 3
        self.assertEqual(limit_day, token_duration.day)
