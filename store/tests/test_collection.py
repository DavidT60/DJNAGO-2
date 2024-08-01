import pytest
from django.contrib.auth.models import User
from store.models import Collection
from model_bakery import baker
from rest_framework import status

@pytest.fixture
def create_collection(action_clinet):
    def make_collection(collection):
        return action_clinet.post('/store/collection/', collection)
    return make_collection

@pytest.fixture
def create_user_authentication(action_clinet):
    def make_authentication(authentication):
        return action_clinet.force_authenticate(user=authentication)
    return make_authentication
create_user_authentication

@pytest.mark.django_db
class TestCreateCollection:
  def test_if_user_has_not_credentials_returns_401(self, create_collection):
        response2 = create_collection({'title':'a'})        
        assert response2.status_code == status.HTTP_401_UNAUTHORIZED
  
  def test_if_user_is_not_admin_retrun_403(self, create_collection, create_user_authentication):
        create_user_authentication({})
        response = create_collection({'title':'a'})        
        assert response.status_code == status.HTTP_403_FORBIDDEN
  
  def test_if_data_is_invalid_retruns_400(self, action_clinet):
    action_clinet.force_authenticate(user=User(is_staff=True, is_superuser=True))
    response = action_clinet.post('/store/collection/', {'title':''})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'] is not None
    


@pytest.mark.django_db
class TestRetriveCollection:
    def test_if_the_collection_is_retrived_retrun_200(self, action_clinet):
        collection = baker.make(Collection)
        action_clinet.force_authenticate(user=User(is_staff=True, is_superuser=True))
        response = action_clinet.get(f'/store/collection/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK 