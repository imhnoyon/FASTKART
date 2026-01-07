# from .models import User
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model=User
        fields = ['id', 'email', 'password', 'first_name',
                  'last_name', 'address', 'phone_number']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model=User
        ref_name='CustomUser'
        fields = ['id', 'email', 'first_name',
                  'last_name', 'address', 'phone_number','is_staff']
        read_only_fields=['is_staff']
        
        
    