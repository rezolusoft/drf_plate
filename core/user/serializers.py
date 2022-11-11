from rest_framework import serializers
from core.user.models import User


class UserSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        """Create and return a new user"""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing user
           We override this methods because of password setting
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('public_id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'position',
                  'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
