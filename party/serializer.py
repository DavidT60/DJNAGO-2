from rest_framework import serializers

from djoser.serializers import UserSerializer as CurrentUser
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer




class UserSerializer(CurrentUser):
    
    class Meta(CurrentUser.Meta):
        fields = ['id','username', 'email', 'first_name', 'last_name']
    
   


class UserCreateSerializer(BaseUserCreateSerializer):
    # value as arguments.#
    
    def validate_username(self, value:str):
          if value.startswith('@') == False:
             raise serializers.ValidationError(f'The User Name must start with @')
          return value
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
    
