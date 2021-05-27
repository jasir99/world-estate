from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers

from .models import User, UserReview
from api.serializers import PropertyAddressSerializer
from api.models import PropertyAddress


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = '__all__'

    def validate(self, attrs):
        reviewingUser = attrs.get('reviewingUser')
        reviewedUser = attrs.get('reviewedUser')
        if reviewedUser == reviewingUser:
            raise serializers.ValidationError('You cannot review yourself!')
        return attrs

    def create(self, validated_data):
        review = UserReview.objects.create(**validated_data)
        return review


class UserSerializer(serializers.ModelSerializer):
    properties = PropertyAddressSerializer(many=True, required=True)
    reviewedUser = UserReviewSerializer(many=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'image', 'properties', 'reviewedUser')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'phone_number')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        client = User.objects.create(**validated_data)
        return client


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password')


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password is not found.')
        try:
            queryset = PropertyAddress.objects.filter(user=user.pk)
            properties_serializer = PropertyAddressSerializer(queryset, many=True)
            update_last_login(None, user)
        except:
            raise serializers.ValidationError('Wrong credentials')
        return {
            'user': user,
            'properties': properties_serializer.data
        }

def get_and_authenticate_user(email, password):
    user = authenticate(email=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    class Meta:
        model = User
        fields = ('email',)

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError('A user with this email is not found.')

        return user


class NewPasswordSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('password',)

    def validate(self, attrs):
        password = attrs.get('password')
        return password


