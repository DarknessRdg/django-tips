from django.contrib.auth.models import User

from rest_framework import status
import rest_framework.test


class APITestCase(rest_framework.test.APITestCase):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

    @property
    def data(self):
        return {
            'username': self.username,
            'password': self.password
        }

    def setUp(self) -> None:
        self.password = '123'
        self.username = 'user test'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def assertSuccess(self, response, msg=""):
        """Asserts given response has a success status code."""
        success = status.is_success(response.status_code)
        if not msg:
            msg = f'error: {str(response.content)}.'

        msg = f'status: [{response.status_code}], {msg}'
        self.assertTrue(success, msg=msg)

    def get_client_method(self, method):
        """
        Returns function to match http method passed through `method` param.

        Args:
            method: String with HTTP method name. Use `self.<HTTP METHOD>` constant.

        Returns:
            function: client method to given http method.
        """
        request_map = {
            self.GET: self.client.get,
            self.POST: self.client.post,
            self.PUT: self.client.put,
            self.PATCH: self.client.patch,
            self.DELETE: self.client.delete
        }
        return request_map[method]

    def assertRequiresAuthentication(self, *args, method=None, **kwargs):
        """
        Asserts given args and kwargs requires user to be authenticated.

        Args:
            *args: Args to be passed to client method
            **kwargs: kwargs to be passed to client method.
            method: String with HTTP method name. Use `self.<HTTP METHOD>` constant.
        """
        assert method is not None, "Missing named parameter `method`."

        self.client.force_authenticate(None)
        fetch = self.get_client_method(method)
        response = fetch(*args, **kwargs)
        status_code = response.status_code

        msg = (f'Method {method} should require authentication but response did not '
               f'returned an authorization error, instead returned {status_code}.')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, status_code, msg)

    def assertNotRequiresAuthentication(self, *args, method=None, **kwargs):
        """
        Asserts given args and kwargs does NOT requires user to be authenticated.

        Args:
            *args: Args to be passed to client method
            **kwargs: kwargs to be passed to client method.
            method: String with HTTP method name. Use `self.<HTTP METHOD>` constant.
        """
        assert method is not None, 'Missing named parameter `method`.'

        fetch = self.get_client_method(method)
        response = fetch(*args, **kwargs)
        status_code = response.status_code

        msg = (f'Method {method} should not require authentication but response '
               f'returned an authorization error: {status_code}.')
        self.assertNotEqual(status.HTTP_401_UNAUTHORIZED, status_code, msg)
