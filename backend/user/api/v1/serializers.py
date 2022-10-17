from django.contrib.auth import authenticate

from rest_framework import serializers

from user.models import User


class ObtainAuthDataSerializer(serializers.ModelSerializer):

    auth_token = serializers.StringRelatedField()
    avatar = serializers.ImageField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)

    username = serializers.CharField(validators=[])
    password = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=False,
        style={'input_type': 'password'},
    )

    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        return user

    class Meta:
        model = User
        fields = (
            'avatar',
            'username',
            'password',
            'last_name',
            'auth_token',
            'first_name',
        )


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'avatar',
            'username',
            'last_name',
            'first_name',
        )


class CreateUserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(required=False)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    bio = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
    )

    last_name = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    auth_token = serializers.StringRelatedField()

    def create(self, validated_data):
        name = validated_data.pop('name')

        if len(split_name := name.split(' ')) > 1:
            first_name, last_name = split_name
        else:
            first_name, last_name = name, ''

        return User.objects.create_user(
            **validated_data,
            last_name=last_name,
            first_name=first_name,
        )

    class Meta:
        model = User
        fields = (
            'bio',
            'name',
            'email',
            'avatar',
            'username',
            'password',
            'last_name',
            'first_name',
            'visibility',
            'auth_token',
        )
