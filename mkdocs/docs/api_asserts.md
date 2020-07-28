# Extra asserts para API testes

Classe útil para extender suas classes de testes que utilizam `APIClient()` para testar os endpoints da sua URL.

The following code can be found [here.](https://github.com/DarknessRdg/django-tips/blob/master/exemplo/app/tests/api_test_case.py)


```py
from rest_framework.settings import api_settings
import rest_framework.test
import json

from django.contrib.auth.models import User

from rest_framework import status
import rest_framework.test


RESULTS_KEY = 'results'
NEXT_KEY = 'next'


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

    @property
    def request(self):
        """Returns a valid request"""
        if self._request is None:
            response = self.client.get('/')
            self._request = response.wsgi_request
        return self._request

    def setUp(self) -> None:
        self.password = '123'
        self.username = 'user test'
        self.user = User.objects.create_user(username=self.username, password=self.password)

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

    def assertMethodAllowed(self, *args, method=None, **kwargs):
        """
        Asserts endpoint return a success status code (between 200 and 299)
        when requesting given method.

        Args:
            *args: Args to be passed to client method
            **kwargs: kwargs to be passed to client method.
            method: String with HTTP method name. Use `self.<HTTP METHOD>` constant.
        """
        assert method is not None, "Missing named parameter `method`."

        fetch = self.get_client_method(method)
        response = fetch(*args, **kwargs)
        status_code = response.status_code
        is_success = status.is_success(status_code)

        msg = (f'Method {method} should be allowed to access, status code returned: {status_code}. '
               f'Response body: {response.content}')
        self.assertTrue(is_success, msg)

    def assertMethodNotAllowed(self, *args, method=None, **kwargs):
        """
        Asserts endpoint return a status code 405 (not allowed) when requesting given method.

        Args:
            *args: Args to be passed to client method
            **kwargs: kwargs to be passed to client method.
            method: String with HTTP method name. Use `self.<HTTP METHOD>` constant.
        """
        assert method is not None, "Missing named parameter `method`."

        fetch = self.get_client_method(method)
        response = fetch(*args, **kwargs)
        status_code = response.status_code

        msg = f'Method {method} should not be allowed to access, status code returned: {status_code}.'
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, status_code, msg)

    def get_serializer_context(self):
        """Returns data to be passed as context to serializer"""
        return {
            'request': self.request
        }

    def assertSuccess(self, response, msg=""):
        """Check the given response has a success status code."""
        success = status.is_success(response.status_code)
        if not msg:
            msg = f'error: {str(response.content)}.'

        msg = f'status: [{response.status_code}], {msg}'
        self.assertTrue(success, msg=msg)

    def assertClientError(self, response, msg=""):
        """Check the given response has a client error status code."""
        client_error = status.is_client_error(response.status_code)
        if not msg:
            msg = f'Response status code is not a client error.'

        msg = f'status: [{response.status_code}], {msg}'
        self.assertTrue(client_error, msg=msg)

    def assertPagination(self, endpoint, queryset, serializer_class, msg=""):
        """
        Check if all pages returns expected data.

        Args:
            endpoint: String to start endpoint.
            queryset: Model Queryset with all instances that should be on pages.
                Remember to order just like view will order, otherwise the result may be different.
            serializer_class: serializer class to get data from each object on queryset.
            msg: Optional. Message to appear when test fail.
        """
        url = endpoint
        count, page_size = queryset.count(), api_settings.PAGE_SIZE

        pages = count // page_size
        if count % page_size != 0:
            pages += 1

        for page in range(pages):
            response = self.client.get(url)
            data = json.loads(response.content)

            queryset_page = queryset[:page_size]
            serializer = serializer_class(queryset_page, many=True, context=self.get_serializer_context())

            for expected, received in zip(serializer.data, data[RESULTS_KEY]):
                self.assertDictEqual(dict(expected), received, msg)

            queryset = queryset.exclude(pk__in=[instance.pk for instance in queryset_page])
            url = data[NEXT_KEY]
```
