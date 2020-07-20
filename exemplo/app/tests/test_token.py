from .api_test_case import APITestCase
from django.urls import reverse
from app.tokens import TokenDoisDiasSerializer


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
