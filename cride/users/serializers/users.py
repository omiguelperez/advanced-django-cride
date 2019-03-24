"""User serializers."""

from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from cride.users.models import User, Profile


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, attrs):
        """Check credentials."""
        user = authenticate(username=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet.')
        self.context['user'] = user
        return attrs

    def create(self, validated_data):
        """Create or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, attrs):
        """Verify password match."""
        passwd = attrs['password']
        passwd_conf = attrs['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Password don\'t match.')
        password_validation.validate_password(passwd)
        return attrs

    def create(self, validated_data):
        """Handle user and profile creation."""
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data, is_verified=False)
        Profile.objects.create(user=user)
        return user
