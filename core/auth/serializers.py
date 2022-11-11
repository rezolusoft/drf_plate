from rest_framework import serializers
from django.contrib.auth import authenticate


class AuthSerializer(serializers.Serializer):
    """
    Token authentication serializer class
    """
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=150, write_only=True)

    def validate(self, attrs):
        """
        Authentication serializer validation
        :param attrs:
        :return:
        """
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            # check out if user provide both credentials
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                error = "Unable to login user with thees credentials"
                raise serializers.ValidationError(error, code='authorization')

        else:
            error = "User must provide a username and a password"
            raise serializers.ValidationError(error, code='authorization')

        attrs['user'] = user
        return attrs
    
    class Meta():
        pass
