import pytest
from django.contrib.auth.models import User
from store.models import Product
from model_bakery import baker
from rest_framework import status



@pytest.mark.django_db
class TestCreateProduct:
    
    
    def test_if_user_credential_returns_401(self, action_clinet):
         response = action_clinet.get('/store/product/')
         assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # def test_if_user_insert_invalid_data_product_retrun_400(self, action_clinet):
    #     response = action_clinet.post('/store/product/', {'product':''})
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST