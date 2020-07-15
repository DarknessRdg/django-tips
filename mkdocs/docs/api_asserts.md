# Extra asserts para API testes

Classe útil para extender suas classes de testes que utilizam `APIClient()` para testar os endpoints da sua URL.


```py
from rest_framework.settings import api_settings
from rest_framework import status


class APITestCase(rest_framework.test.APITestCase):
    """
    Base API class with additional asserts methods for response and other
    helpers methods and property.
    """
    _request = None  # cache request

    @property
    def request(self):
        """Returns a valid request that can be helpfull with serializers context"""
        if self._request is None:
            response = self.client.get('/')
            self._request = response.wsgi_request
        return self._request

    def get_serializer_context(self):
        """Returns data to be passed as context to serializer"""
        return {
            'request': self.request
        }

    def assertSuccess(self, response, msg=""):
        """Asserts given response has a success status code."""
        success = status.is_success(response.status_code)
        if not msg:
            msg = f'error: {str(response.content)}.'

        msg = f'status: [{response.status_code}], {msg}'
        self.assertTrue(success, msg=msg)

    def assertClientError(self, response, msg=""):
        """Asserts given response has a client error status code."""
        client_error = status.is_client_error(response.status_code)
        if not msg:
            msg = f'Response status code is not a client error.'

        msg = f'status: [{response.status_code}], {msg}'
        self.assertTrue(client_error, msg=msg)

    def assertPagination(self, endpoint, queryset, serializer_class, msg=""):
        """
        Asserts if all pages returns expected data.

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