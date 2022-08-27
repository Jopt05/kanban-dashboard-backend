from tkinter.ttk import Style
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ User serializer """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                "write_only": True,
                "min_length": 5
            }
        }

    def create(self, validated_data):
        """ Create new user with encrypted password and return """
        return get_user_model().objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """ Login serializer """

    email = serializers.CharField()
    password = serializers.CharField(
        style={
            "input_type": "password"
        },
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ Validate and auth """
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _("Unable to auth with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

        return attrs
