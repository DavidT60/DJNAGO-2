import pytest
from rest_framework.test import APIClient

@pytest.fixture
def action_clinet():
    print("Actionn Fixture")
    return APIClient()
