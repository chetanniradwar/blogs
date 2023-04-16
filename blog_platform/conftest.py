import pytest
from rest_framework.test import APIClient
from django.test.client import RequestFactory


@pytest.fixture(scope='session')
def api_client():
    return APIClient()


@pytest.fixture(scope='session')
def request_factory():
    return RequestFactory()
